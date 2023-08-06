from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from .. import pipeline as p
from ..utils import dotdict
import multiprocess as mp
import socket
import os
import yaml
import logging

log = logging.getLogger(__name__)

# _creds (in .gitignore)
HERE = os.path.dirname(__file__)
creds = dotdict(yaml.safe_load(open(f"{HERE}/_creds.yaml")))


def start(address, port):
    """ start ftp server as background process """

    def target(address, port):
        from defaultlog import logging

        log = logging.getLogger(__name__)

        authorizer = DummyAuthorizer()
        authorizer.add_user(creds.username, creds.password, p.root, perm="elradfmw")
        handler = FTPHandler
        handler.authorizer = authorizer
        server = FTPServer((address, port), handler)
        server.serve_forever()

    p = mp.Process(target=target, args=(address, port))
    p.start()


def set_ftp(
    address=socket.gethostbyname(socket.getfqdn()), port=4100, path="pipemaker"
):
    """ switch filesystem to ftp
    :param address: ip address
    :param port: port
    :param path: root path for ftp server
    """
    log.info("setting ftp")

    # datapath is included in filesystem not path. typically an ftp server exposes a specific folder.
    p.fpath = "{filesystem}|{job}/{name}{extension}"
    p.filesystem = f"ftp://{creds.username}:{creds.password}@{address}:{port}/{path}"
    start(address, port)
