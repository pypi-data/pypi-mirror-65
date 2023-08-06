import fs
from fs.copy import copy_file
import pandas as pd

# blog-process remove on next release. bug.
import fs.osfs
import logging

log = logging.getLogger(__name__)


def save(self, obj, fpath, func):
    """ save pandas dataframe to format defined by func e.g. csv, excel
    For remote url it will save locally then upload

    :param obj: data to save
    :param fpath: destination filepath
    :param func: dataframe save function e.g. to_csv
    """
    func = getattr(obj, func)
    path = fpath.path.lstrip("/")

    # save locally
    if isinstance(self.ofs, fs.osfs.OSFS):
        self.ofs.makedirs(fs.path.dirname(path), recreate=True)
        func(path)
        return

    # save to local cache then upload
    local = fs.open_fs("")
    cache = f"cache/{path}"
    local.makedirs(fs.path.dirname(cache), recreate=True)
    func(cache)
    copy_file(local, cache, self.fs, path)


def load(self, func):
    """ load pandas dataframe from format defined by func e.g. csv, excel
    For remote url it will read local cache; OR download then read
    The cache allows downstream tasks to use cache data if available

    :param func: pandas function for loading e.g. read_csv
    """

    func = getattr(pd, func)
    path = self.path.lstrip("/")

    # read locally
    if isinstance(self.ofs, fs.osfs.OSFS):
        return func(path)

    # load from local cache or download
    local = fs.open_fs("")
    cache = f"cache/{path}"
    if not local.exists(cache):
        local.makedirs(fs.path.dirname(cache), recreate=True)
        copy_file(self.fs, path, local, cache)
    return func(cache)
