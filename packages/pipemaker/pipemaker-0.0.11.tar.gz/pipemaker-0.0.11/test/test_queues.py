from multiprocessing import Process
from time import sleep

from pipemaker.master import *
from . import module
from .module import *
from pipemaker.utils.defaultlog import log


def stop_soon(Q, delay=2):
    log.info(f"stopping after {delay} seconds")
    sleep(delay)
    q = Q()
    q.stop()


def test_rabbitq_put():
    from pipemaker.consumer import Rabbitq
    Rabbitq().channel.queue_delete("Rabbitq")

    # put messages on queue
    from pipemaker.producer import Rabbitq
    q = Rabbitq()
    q.queue = q.channel.queue_declare(queue=q.name, auto_delete=True)

    q.put("hello")
    q.put("again")

    # list messages
    from pipemaker.consumer import Rabbitq
    q = Rabbitq()
    q.queue = q.channel.queue_declare(queue=q.name, auto_delete=True)
    assert q.list() == ["hello", "again"]

def test_rabbitq_get(caplog):
    # listen for messages
    from pipemaker.consumer import Rabbitq
    q = Rabbitq()

    caplog.clear()
    log.info("get")
    p = Process(target=stop_soon, args=(Rabbitq,))
    p.start()
    q.start_consuming_process()
    log.info(caplog.messages)
    expected = ["get", "start consuming", "hello", "again", "stop consuming"]
    for message, expected in zip(caplog.messages, expected):
        assert message.startswith(expected)

def test_responseq():
    from pipemaker.producer import Responseq
    q = Responseq("10")
    q.put("hi")
    q = Responseq("20")
    q.put("there")

    from pipemaker.consumer import Responseq
    assert Responseq("10").listen() == "hi"
    assert Responseq("20").listen() == "there"
#
#
# def test_task():
#     # todo make fixture
#     p = pipeline
#     p.start()
#     env.mode = "a"
#
#     # add task
#     p.add(module)
#     make_test()
#
#     # check task completed
#     from pipemaker.producer import Schedulerq
#     s = Schedulerq()
#     df = s.view()
#     row = df[df.url==module.make_test.output.url].iloc[0]
#     assert row["name"] == "test"
#     assert row.status == "completed"
#     assert row.finished >= row.started
#     assert row.progress == "100%"