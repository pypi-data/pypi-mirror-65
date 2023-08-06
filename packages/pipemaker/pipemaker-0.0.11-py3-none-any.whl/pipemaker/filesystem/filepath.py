import fs
import fs.path
from fs.opener.parse import parse_fs_url
import importlib
from functools import partial
from collections import UserString
from urllib.parse import urlencode
from pipemaker.utils.dotdict import dotdict

import logging

log = logging.getLogger(__name__)

# dict(url=connection) cache to reuse connections
cons = dict()


class Fpath(UserString):
    """ a fstring that will be formatted into a Filepath. methods return Fpath objects
    Used to distinguish path strings from strings when passed to functions or printed
    """

    def __repr__(self):
        """ with class """
        log.info(9999)
        return f"Fpath({self})"


class Filepath:
    """ wraps pyfilesystem fs_url

        consistent api for all urls without having to consider the filesystem
        * one step filepath methods for filesystem and filesystem/path e.g. exists, isdir
        * additional filepath methods e.g. load, save
        without this code has to apply separate tasks to filesystem and path
    """

    def __init__(self, url):
        """
        typically split automatically based on content
        * osfs:// (default)
        * osfs://c: (for windows to include drive)
        * googledrive://?client_secret=xxx&access_token=xxx&refresh_token=xxx
        * s3://bucket
        * ftp://username:password@ipaddress:port

        can also split explicitly using | (extension to fs_url spec)
        self.path always starts with /
        """
        # main split
        self.fs = None
        self.path = None
        # full split of protocol, username etc..
        self.parsed = None

        # make default filesystem explicit
        if "://" not in url:
            url = f"osfs://{url}"

        # explicitly split filesystem/path
        if "|" in url:
            self.fs, self.path = url.split("|")
            return

        # parse url
        self.parsed = dotdict(parse_fs_url(url)._asdict())
        p = self.parsed

        # standardise
        p.protocol = p.protocol.lower()
        p.path = p.resource.lstrip("/")
        p.path = p.path.replace("\\", "/")
        p.path = fs.path.normpath(p.path)

        # include creds in fs
        # s3, ftp
        if p.username:
            self.fs = f"{p.protocol}://{p.username}:{p.password}@"
        # googledrive
        elif p.params:
            self.fs = f"{p.protocol}://?{urlencode(p.params)}"
        # osfs
        else:
            self.fs = f"{p.protocol}://"

        # split fs and path. this is not currently in parsed.
        p.path = p.path.split("/")

        # ftp include address
        if p.protocol == "ftp":
            address = p.path.pop(0)
            self.fs = f"{p.protocol}://{address}"

        # s3 include bucket
        if p.protocol == "s3":
            bucket = p.path.pop(0)
            self.fs = f"{p.protocol}://{bucket}"

        # windows include drive
        if p.protocol == "osfs":
            if p.path[0].endswith(":"):
                drive = p.path.pop(0)
                self.fs = f"{p.protocol}://{drive}"

        # remaining p.path after extracting filesystem elements
        p.path = "/".join(p.path)
        self.path = "/" + p.path

    def __getstate__(self):
        """ required for pickle """
        return self.__dict__

    def __setstate__(self, d):
        """ required for pickle """
        self.__dict__ = d

    @property
    def ofs(self):
        """ return open filesystem here rather than __init__ as cannot be pickled """
        global cons
        # cache connections as 500ms overhead
        cons[self.fs] = cons.get(self.fs, fs.open_fs(self.fs))

        # clear cache
        if len(cons) > 100:
            cons.pop(cons.keys()[0])

        return cons[self.fs]

    @property
    def url(self):
        """ filesystem and path. """
        if self.parsed.params:
            return f"{self.fs}{self.path}?{urlencode(self.parsed.params)}"
        return f"{self.fs}{self.path}"

    def __repr__(self):
        """ class and url """
        return f"Filepath({self.url})"

    def __str__(self):
        """ basename without extension. useful for display as short name """
        filename = fs.path.basename(self.path)
        return fs.path.splitext(filename)[0]

    def __hash__(self):
        """ unique key for dict """
        return hash(self.url)

    def __eq__(self, other):
        """ equal if have same url """
        return self.url == other.url

    def __getattr__(self, method):
        """ shortcut to ofs.method(path, *args, **kwargs) """
        return partial(getattr(self.ofs, method), self.path)

    def _get_driver(self, driver=None):
        """
        :param driver: name of driver to load/save. if None uses file extension or pkl
        :return: driver module
        """
        if driver is None:
            driver = fs.path.splitext(self.path)[-1] or ".pkl"
            driver = driver[1:]
        try:
            return importlib.import_module(f"pipemaker.filesystem.filedrivers.{driver}")
        except ModuleNotFoundError:
            log.error(
                f"No driver found for {driver}. You can _add_module one in the filedrivers folder."
            )
            raise

    def load(self, driver=None):
        """ return file contents
        :param driver: function to load/save. if None uses file extension or pkl """
        driver = self._get_driver(driver)
        return driver.load(self)

    def save(self, obj, driver=None):
        """ save obj to file
        :param driver: function to load/save. if None uses file extension or pkl
        """
        # save to temp file so file is not visible until complete.
        dirname, filename = fs.path.split(self.path)
        self.ofs.makedirs(fs.path.dirname(self.path), recreate=True)
        temp_fpath = Filepath(f"{dirname}/temp_filepath_{filename}")
        driver = self._get_driver(driver)
        driver.save(self, obj, temp_fpath)
        temp_fpath.move(self.path)
