import inspect
from graphviz import Digraph
from datetime import datetime
import sys

from ..filesystem import Filepath, Fpath
from ..worker import Task

# multiprocessing
import multiprocessing as mp
from ..consumer import Responseq
from ..producer import Schedulerq
from .multiprocess import mp_enabled, requires_mp

import logging

log = logging.getLogger(__name__)

schedulerq = None
if mp_enabled:
    schedulerq = Schedulerq()


class Runner:
    """
    Identifies upstream tasks; submits tasks to scheduler or executes synchronously
    """

    def __init__(self, pipeline, func):
        """
        :param pipeline: parent pipe used to find the source function for a file
        :param func:    function to wrap
        """
        self.pipeline = pipeline
        self.func = func

        # output path. required here as pipe uses it as a unique id
        sig = inspect.signature(func)
        if sig.return_annotation != inspect.Parameter.empty:
            self.oname = sig.return_annotation
        elif self.func.__name__.startswith("make_"):
            self.oname = self.func.__name__[len("make_") :]
        elif self.func.__name__.startswith("get_"):
            self.oname = self.func.__name__[len("get_") :]
        else:
            self.oname = self.func.__name__

    def __repr__(self):
        """ :return func(**params)->output """
        params = ",".join(
            str(p) for p in inspect.signature(self.func).parameters.values()
        )
        return f"{self.func.__name__}({params})->{repr(self.parse_output())}"

    def __call__(self, *args, **kwargs):
        """ called in same way as underlying function would be called e.g. make_thing(5, a=3)
        used for initiating task only. upstream tasks called via run
        """
        # validate
        if self.pipeline.mode not in ("s", "a", "aw"):
            raise Exception("Invalid self.pipeline.mode")

        # check output exists
        self.output = self.parse_output()
        if self.output.exists():
            if self.pipeline.mode == "a":
                return
            elif self.pipeline.mode in ["s", "aw"]:
                return self.output.load()

        # run task
        if self.pipeline.mode == "s":
            return self.run_s(*args, **kwargs)

        elif self.pipeline.mode == "a":
            self.run_a(*args, **kwargs)
            return

        elif self.pipeline.mode == "aw":
            self.run_a(*args, **kwargs)
            self.wait()
            return self.output.load()

    def run_s(self, *args, **kwargs):
        """ run tasks synchronously """
        inputs = self.parse_inputs(*args, **kwargs)
        output = self.parse_output()

        # load
        indata = dict()
        for k, v in inputs.items():
            if not isinstance(v, Filepath):
                indata[k] = v
            elif v.exists():
                indata[k] = v.load()
            else:
                utask = self.pipeline._output2runner.get(k)
                if not utask:
                    log.error(f"missing {k}")
                    sys.exit(0)
                indata[k] = utask.run_s(*args, **kwargs)

        # execute and save
        log.info(f"creating {output.url}")
        outdata = self.func(**indata)
        output.save(outdata)
        return outdata

    @requires_mp
    def run_a(self, *args, **kwargs):
        """ submit tasks to scheduler for asynchronous processing on multiple cpus """
        # validate parameters including upstream pipe
        tasks = dict()
        missing = []
        self.get_tasks(tasks, missing, *args, **kwargs)
        if missing:
            log.error(f"Missing inputs {missing}")
            sys.exit(0)

        body = dict(
            tasks=tasks,
            time=datetime.now(),
            event="onRun",
            process=mp.current_process().name,
            source="runner",
        )
        schedulerq.put(body)

    def get_tasks(self, tasks, missing, *args, **kwargs):
        """ recursively get tasks and missing for upstream pipe
        enables all missing parameters to be identified before execution

        :param tasks: dict(url=task) that is populated recursively
        :param missing: list of missing parameters populated recursively
        :param args: args passed on execution
        :param kwargs: kwargs passed on execution
        """
        # create scheduler task
        output = self.parse_output()
        inputs = self.parse_inputs(*args, **kwargs)
        task = Task(self.func.__module__, self.func.__name__, inputs, output)
        task.upstream = set()
        task.downstream = set()
        task.path = self.pipeline.path
        task.name = str(task.output)
        task.url = task.output.url
        tasks[task.url] = task

        # process inputs
        for k, v in inputs.items():
            # existing input data
            if not isinstance(v, Filepath) or v.exists():
                continue
            # get runner to make data
            arg = self.pipeline._output2runner.get(k)
            if not arg:
                # no runner found i.e. missing input data
                missing.append(k)
            else:
                # add runner to upstream tasks
                upstream_url = arg.parse_output().url
                if upstream_url not in tasks:
                    arg.get_tasks(tasks, missing)
                task.upstream.add(upstream_url)
                tasks.get(upstream_url).downstream.add(task.url)

    @requires_mp
    def wait(self):
        """ wait for task to finish
        Usage:: wait for output before proceeding to next cell in notebook
        """
        if self.output.exists():
            return
        Responseq(self.output.url).listen()

    def parse_output(self):
        """ path to output file """
        p = self.pipeline
        v = getattr(p, self.oname, p.fpath)
        if isinstance(v, Filepath):
            return v
        return Filepath(v.format(name=self.oname, **vars(p)))

    def parse_inputs(self, *args, **kwargs):
        """ return inputs

        :param args:    args passed to function at runtime
        :param kwargs:  kwargs passed to function at runtime
        :return:        dict of name=value where value is parameter value or filepath

        inputs can be data, Fpath or Filepath.
        They are populated from::
            * runtime args/kwargs
            * global parameter e.g. pipeline.input=2
            * default parameter e.g. def myfunc(input1=2)
            * default Fpath
        Each Fpath is formatted using vars(pipeline) to create a Filepath
        """
        p = self.pipeline

        # run_time args and arguments as passed above.
        sig = inspect.signature(self.func)

        # map *args, **kwargs onto signature. partial as some are set in env rather than passed directly.
        bind = sig.bind_partial(*args, **kwargs)
        arguments = bind.arguments.copy()

        # fill parameters. they can be data, Fpath or Filepath
        # iterate over sig to map parameters to env
        #     bind.args has no name so cannot map parameter name to Fpath. bind.kwargs cannot be updated.
        #     bind.arguments excludes default parameters and does not expose kwargs key
        for k, v in sig.parameters.items():
            # flatten kwargs
            if v.kind == v.VAR_KEYWORD:
                arguments.update(arguments[k])
                del arguments[k]
                continue

            # bound from function call
            if k in arguments:
                pass
            # global specific to parameter
            elif hasattr(p, k):
                arguments[k] = getattr(p, k)
            # default parameter
            elif v.default != inspect.Parameter.empty:
                arguments[k] = v.default
            # global default
            else:
                arguments[k] = p.fpath

        # convert Fpath to Filepath
        arguments = {
            k: Filepath(v.format(name=k, **vars(p))) if isinstance(v, Fpath) else v
            for k, v in arguments.items()
        }

        return arguments

    def view(self, g=None, parents=False):
        """ return graphviz display of upstream pipe

        :param g: existing graph. passed recursively to view parents
        :param parents: False views tasks that need to be run. True views all upstream tasks
        """
        p = self.pipeline

        # create graph on first call
        if g is None:
            g = Digraph(strict=True, comment=f"{self.func.__name__} pipe")

        # display formats
        func_style = dict(shape="oval", style="filled", fillcolor="lightgrey")
        exists_style = dict(
            shape="folder",
            height=".1",
            width=".1",
            style="filled",
            fillcolor="lightgreen",
        )
        missing_style = dict(shape="folder", height=".1", width=".1", style="")
        pexists_style = dict(shape="box", style="filled", fillcolor="lightgreen")
        pmissing_style = dict(shape="box", style="")

        # function
        g.node(self.func.__name__, **func_style)

        # inputs
        inputs = self.parse_inputs()
        for k, v in inputs.items():
            if isinstance(v, Filepath):
                if v.exists():
                    g.node(k, **exists_style)
                    g.edge(k, self.func.__name__)
                    if parents:
                        pw = p._output2runner.get(k)
                        if pw is not None:
                            pw.view(g, parents)
                else:
                    upstream = p._output2runner.get(k)
                    if upstream:
                        # no file but a task can create it
                        upstream.view(g, parents)
                        g.edge(k, self.func.__name__)
                    else:
                        # no parameter. no file. no task to create it.
                        g.node(k, **pmissing_style)
                        g.edge(k, self.func.__name__)
            else:
                # supplied parameter
                g.node(k, **pexists_style)
                g.edge(k, self.func.__name__)

        # output
        output = self.parse_output()
        if output.exists():
            g.node(str(output), **exists_style)
        else:
            g.node(str(output), **missing_style)

        g.edge(self.func.__name__, str(output))

        return g
