from ..filesystem.filepath import Filepath
from ..producer import Schedulerq
import inspect
import multiprocess as mp
from datetime import datetime
import logging

log = logging.getLogger(__name__)


class Task:
    """
    minimal executable that gets passed to task queue

    * load data, run function, save result (all run locally).
    * trigger events to be actioned on master or elsewhere.

    within runner and scheduler this includes metadata:
        job:        job pipe
        status:     waiting, ready,
                    loading, running, saving,
                    completed, failed, failed_upstream
        upstream:   list of urls for upstream tasks not yet completed
        downstream: list of urls for downstream tasks
        details:    only used to display messages e.g. list of upstream tasks, error message.
        process:    name of process on which it ran
        started:    time run started
        finished:   time run finished
    """

    def __init__(self, module, func, inputs, output):
        """
        :param module: name of module
        :param func: name of func
        :param inputs: data or filepaths to be loaded
        :param output: filepath
        """
        # needed to run task
        self.module = module
        self.func = func
        self.inputs = inputs
        self.output = output

        # metadata for scheduler
        self.job = None
        self.status = None
        self.upstream = None
        self.downstream = None
        self.process = None
        self.started = None
        self.finished = None
        self.progress = None

    def __str__(self):
        """ function name """
        return str(self.output)

    def __repr__(self):
        """ with class and filesystem """
        return f"Task({self.output.url})"

    @property
    def workertask(self):
        """ clean version of task for execution """
        return Task(self.module, self.func, self.inputs, self.output)

    def run(self):
        """ execute in worker_process process """
        self.scheduler = Schedulerq()
        try:
            self.load()
            self.execute()
            self.save()
            self.onEvent("onComplete")
            return self.outdata
        except Exception as e:
            log.exception(f"exception in {self.output.path}\ne")
            self.onEvent("onError", exception=e)
            return
        finally:
            self.scheduler.connection.close()

    def load(self):
        """ load data from filepaths """
        self.onEvent("onLoading")

        # load func
        from importlib import import_module

        module = import_module(self.module)
        self.func_method = getattr(module, self.func)

        # load data
        self.indata = {
            k: v.load() if isinstance(v, Filepath) else v
            for k, v in self.inputs.items()
        }

    def execute(self):
        """ import module and execute function """
        self.onEvent("onRunning")
        self.outdata = self.func_method(**self.indata)

    def save(self):
        """ save data to filepath """
        self.onEvent("onSaving")
        self.output.save(self.outdata)

    def onEvent(self, event, **kwargs):
        """ send event message

        :param event: string e.g. "onError"
        :param kwargs: optional dict of event data e.g. time, process, url
        """
        kwargs = dict(kwargs)
        kwargs["time"] = datetime.now()
        kwargs["event"] = event
        kwargs["process"] = mp.current_process().name
        kwargs["source"] = self.output.url
        self.scheduler.put(kwargs)


# events callled from running task ##################################


def onEvent(event, **kwargs):
    """ fire event from task function via workertask wrapper
    e.g. in function onEvent("doneThat", result=4)
    """
    self = inspect.currentframe().f_back.f_back.f_locals["self"]
    # disable in synchronous mode
    if not isinstance(self, Task):
        return
    return self.onEvent(event, **kwargs)


def progress(i, total):
    """ reports progress at iteration i/total """
    self = inspect.currentframe().f_back.f_back.f_locals["self"]
    # disable in synchronous mode
    if not isinstance(self, Task):
        return
    # every 1%. +1 avoids div zero exception
    if i % (total // 100 + 1) == 0:
        self.onEvent("onProgress", progress=i * 100 // total)
