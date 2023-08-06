import inspect
import types
from .runner import Runner
from .multiprocess import requires_mp, start
from ..filesystem import Filepath, Fpath

import logging

log = logging.getLogger(__name__)


class Pipeline:
    """ pipeline of runners that convert inputs into outputs """

    def __init__(self):
        """
        fpath: any user defined fstring that is formatted at runtime with name and vars(pipeline).
        Default is "{fs}/{root}/{path}/{name}{ext}"::

            fs: pyfilesystem e.g. osfs://, s3://, googledrive://, ftp://
            root: root data path. absolute or relative to cwd. Cannot be outside cwd.
            path: subpath to separate runs e.g. pilot, full; london, paris; january, february
            name: filled with name of function output often func.__name__
            ext: output file format e.g. .pkl, .xlsx

        mode: s=sync, a=async. aw=async and wait e.g. pause notebook before next cell.

        rest of pipeline attributes are used to fill parameters at runtime. Example usage::

            * value used as a parameter for a function or any upstream function
            * Filepath to map a data item shared by multiple runs to a common location
            * Filepath to map a file to a remote location
        """
        self.fpath = "{fs}/{root}/{path}/{name}{ext}"

        # these are the defaults used to fill fpath at runtime
        # the fpath can be set to any fstring. it will be filled at runtime by vars(pipeline) + name
        self.fs = "osfs://"
        self.root = "pipedata"
        self.path = ""
        self.ext = ".pkl"
        self.mode = "s"

        # map output to function that can produce it
        self._output2runner = dict()

        # check new members to highlight spelling errors
        self._check_new = True

    def __setattr__(self, key, value):
        if key == "name":
            raise Exception(
                "cannot set name as this would conflict with pipeline data item name"
            )

        # check new members to highlight spelling errors as unusual to add new members
        if hasattr(self, "_check_new") and self._check_new and not hasattr(self, key):
            log.warning(f"creating new pipeline parameter {key}")

        super().__setattr__(key, value)

    @property
    def fpath(self):
        return self._fpath

    @fpath.setter
    def fpath(self, value):
        """ can be set as string or Fpath """
        if isinstance(value, str):
            value = Fpath(value)
        self._fpath = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode in ["a", "aw"]:
            requires_mp(lambda: None)()
            start()
        self._mode = mode

    def add(self, runners, strict=False):
        """ add runners to the pipe
        :param runners: module, list of modules, function, list of functions
        :param strict: if true then exclude functions unless return annotation or start get_, make_
        ..warning:: refers to calling frame so if moved then need to update the code to refer to correct frame
        """
        frame = inspect.currentframe()
        globals = frame.f_back.f_globals

        # convert single runner to list
        if not isinstance(runners, list):
            runners = [runners]

        for runner in runners:
            # already added
            if isinstance(runner, Runner):
                continue

            # invalid parameter
            if not inspect.ismodule(runner) and not inspect.isfunction(runner):
                raise Exception("add parameter should be either a module or a function")

            # add function
            if inspect.isfunction(runner):
                if (
                    not runner.__name__.startswith("_")
                    and runner.__name__ in globals
                    and globals[runner.__name__].__module__ == runner.__module__
                ):
                    # add local ref e.g. func
                    globals[runner.__name__] = self._add_func(runner)
                else:
                    # add local module ref e.g. xxx.func
                    try:
                        fullname = runner.__module__.split(".")
                        setattr(
                            globals[fullname[-1]],
                            runner.__name__,
                            self._add_func(runner),
                        )
                    except:
                        raise Exception(f"cannot find {runner} in globals")
            else:
                # add all functions in module (import module)
                funcs = {
                    k: v
                    for k, v in vars(runner).items()
                    if isinstance(v, types.FunctionType)
                    and not v.__name__.startswith("_")
                    and (v.__module__ == runner.__name__)
                }
                for k, v in funcs.items():
                    # check excluded
                    if strict:
                        sig = inspect.signature(v)
                        if not (
                            sig.return_annotation != inspect.Parameter.empty
                            or v.__name__.startswith("make_")
                            or v.__name__.startswith("get_")
                        ):
                            continue
                    setattr(runner, k, self._add_func(v))

                # add local module reference (from module import *)
                try:
                    for k, v in globals.items():
                        if (
                            # user functions starting _ are assumed not part of a pipe
                            not k.startswith("_")
                            and isinstance(v, types.FunctionType)
                            # only add if part of this module
                            and v.__module__ == runner.__name__
                        ):
                            globals[k] = self._add_func(v)
                finally:
                    del frame

    def name2filepath(self, name):
        """ convert name to filepath
        :param name: internal pipe name
        :return: pyfs filepath to physical location
        """
        path = getattr(self, name, self.fpath).format(name=name, **vars(self))
        return Filepath(path)

    def load(self, name):
        """ load data
        :param name: internal pipe name
        :return: contents of file
        """
        fp = self.name2filepath(name)
        try:
            return fp.load()
        except FileNotFoundError:
            log.error(f"File not found {self.url}")

    def save(self, obj, name):
        """ save data
        :param obj: data to save
        :param name: filename or pyfs url
        """
        fp = self.name2filepath(name)
        fp.save(obj)

    def _add_func(self, f, *args, **kwargs):
        """ decorator that wraps a function to create a Runner """
        runner = Runner(self, f, *args, **kwargs)
        if not hasattr(runner, "oname"):
            log.warning(f"{f.__name__} has no oname so not included in pipe")
            return f
        # store so runners can search for upstream runners to _add_func their inputs.
        self._output2runner[runner.oname] = runner
        return runner


pipeline = Pipeline()
