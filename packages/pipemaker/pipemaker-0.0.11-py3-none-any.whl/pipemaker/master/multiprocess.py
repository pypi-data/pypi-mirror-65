""" tools to start and stop scheduler, workers, web server """

import subprocess
import shlex
import pika
import os

from ..filesystem import Filepath
from ..consumer import Schedulerq, Workerq, Logq
from ..utils import get_name
from ..web import view

import logging

log = logging.getLogger(__name__)


def subprocess_run(cmd):
    cmd = shlex.split(cmd)
    subprocess.run(cmd, capture_output=True, check=True, shell=True)


# check rabbitmq available
mp_enabled = False
try:
    subprocess_run("rabbitmqctl status")
    mp_enabled = True
except:
    pass


def requires_mp(func):
    """ decorator to disable function and log error if mutliprocessing unavailable."""

    def wrapped(*args, **kwargs):
        if not mp_enabled:
            log.error(
                "to use multiprocessing please install rabbitmq and restart pipemaker"
            )
            return
        return func(*args, **kwargs)

    return wrapped


###############################################################################################


@requires_mp
def start(n=None):
    """ start logging, scheduler, workers, view
    :param n: workers required including ones already running
    """
    # queues
    for Q in [Schedulerq, Logq]:
        try:
            connection = pika.BlockingConnection()
            channel = connection.channel()
            channel.queue_declare(Q.__name__, passive=True)
        except pika.exceptions.ChannelClosedByBroker:
            Q.start_consuming_process()
        finally:
            connection.close()

    # workers
    if n is None:
        n = os.cpu_count()
    try:
        connection = pika.BlockingConnection()
        channel = connection.channel()
        current = channel.queue_declare(
            Workerq.__name__, passive=True
        ).method.consumer_count
        connection.close()
    except pika.exceptions.ChannelClosedByBroker:
        current = 0
    n = n - current
    if n <= 0:
        return
    name = get_name()
    log.info(f"starting workers {name} n={n}")
    for i in range(n):
        Workerq.start_consuming_process(f"{name}_{i}")

    connection.close()

    # web server
    view.start()


@requires_mp
def stop():
    """ delete temp files, delete queues, stop web server """
    # files
    cleanup()

    # queues
    log.info("deleting queues")
    connection = pika.BlockingConnection()
    channel = connection.channel()
    for Q in [Schedulerq, Workerq, Logq]:
        channel.queue_delete(Q.__name__)
    connection.close()

    # web server
    view.stop()


@requires_mp
def kill():
    """ restart rabbitmq deleteing all queues.
    .. warning:: this is the nuclear option for testing
    """
    log.info("restarting rabbitmq broker")
    subprocess_run("rabbitmqctl stop_app")
    subprocess_run("rabbitmqctl reset")
    subprocess_run("rabbitmqctl start_app")


def cleanup(root=None, check=False):
    """ cleanup all temp folders
    :param check: ask for confirmation before stop
    """
    from pipemaker import pipeline as p

    if root is None:
        root = p.root
    fp = Filepath(root)
    globber = fp.ofs.glob(f"{fp.path}/**/temp_filepath_*")
    folders = "\n".join([f.path for f in globber])
    if not folders:
        log.info("no temp folders to delete")
        return
    r = "y"
    if check:
        r = input(
            f"Cleanup will stop the following temp folders. Please enter y to confirm.\n{folders}\n"
        )
    if r == "y":
        globber.remove()
        log.info("deleted temp folders")
    else:
        log.info("cancelled deletion of temp folders")


# todo review rabbit api requests versus object calls
"""
# rabbitmq-plugins enable rabbitmq_management
# rabbitmqctl add_user simonm3 simonm3
# rabbitmqctl set_user_tags simonm3 administrator
import requests
from requests.auth import HTTPBasicAuth
r = requests.get("http://localhost:15672/api/queues", auth=HTTPBasicAuth('simonm3', 'simonm3'))
queues = r.json()
names = [q["name"] for q in queues]
workerq = [q for q in queues if q["name"]=="Workerq"][0]
n_workers = workerq["consumers"]
"""
