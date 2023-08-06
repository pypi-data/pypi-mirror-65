from time import sleep

from pipemaker.master import *
from pipemaker.utils.defaultlog import log


def task1(delay) -> "out":
    """ mock task """
    sleep(delay)
    return


def test_multitask():
    p = pipeline
    p.start()
    p.add(task1)

    # add tasks with first task delayed
    env.mode = "a"
    delays = [8, 0, 0, 0, 0, 0, 0]
    for n in range(7):
        env.fvars.job = f"delay{n}"
        task1(delay=delays[n])
        if n == 0:
            longtask = task1

    longtask.wait()

    # assert all completed and first submitted completed last
    from pipemaker.consumer import Schedulerq
    s = Schedulerq()
    df = s.view()
    assert all(df.status=="completed")
    last = df[df.name == "out"].sort_values("finished").iloc[-1].job
    assert last == "delay0"
