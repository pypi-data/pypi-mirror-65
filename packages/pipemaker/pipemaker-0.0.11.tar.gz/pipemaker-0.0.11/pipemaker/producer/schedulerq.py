from . import Rabbitq
from ..consumer import Responseq
import pandas as pd
from uuid import uuid4
from datetime import datetime

import logging

log = logging.getLogger(__name__)


class Schedulerq(Rabbitq):
    """ queue that schedules new tasks; and responds to events from existing tasks

    * tasks from any worker_process can put events on the scheduler
    * updates the central database, launches jobs that were waiting
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = self.channel.queue_declare(queue=self.name, auto_delete=True)

    def get_tasks(self):
        """ get the tasks dict from scheduler. sends message to schedulerq; waits for response
        :return: dict of tasks
        """
        # request tasks from scheduler
        key = str(uuid4())
        self.put(dict(event="onView", key=key))
        r = Responseq(key)
        # timeout returns control to caller if there is some issue
        tasks = r.listen(auto_ack=True, timeout=10)
        return tasks

    def view(self):
        """ get tasks and format as dataframe
        :return: dataframe of tasks
        """
        tasks = self.get_tasks()
        if tasks is None:
            return "no tasks found"

        # format tasks
        # todo remove path to make more generic for fpaths
        df = pd.DataFrame.from_dict([t.__dict__ for t in tasks.values()])
        cols = [
            "url",
            "path",
            "name",
            "status",
            "process",
            "started",
            "finished",
            "elapsed",
            "remaining",
            "progress",
            "details",
        ]
        for col in set(cols) - set(df.columns):
            df[col] = None

        df.started = pd.to_datetime(df.started, errors="coerce")
        df.finished = pd.to_datetime(df.finished, errors="coerce")

        # calculated columns
        started = df.started.fillna(datetime.now())
        finished = df.finished.fillna(datetime.now())
        df["elapsed"] = (finished - started).dt.total_seconds() // 60
        df["remaining"] = df.elapsed / df.progress * 100 - df.elapsed
        if "upstream" in df.columns:
            # for waiting tasks set details=upstream
            df.loc[df.status == "waiting", "details"] = df.upstream.apply(
                lambda upstream: ",".join([str(tasks[url]) for url in upstream])
            )

        # not running
        df.loc[df.started.isnull(), "elapsed"] = None
        df.loc[df.started.isnull() | df.finished.notnull(), "remaining"] = None

        # formatting
        df.progress = df[df.progress.notnull()].progress.apply(
            lambda x: str(int(x)) + "%"
        )
        df.started = df.started[df.started.notnull()].dt.strftime("%H:%M")
        df.finished = df.finished[df.finished.notnull()].dt.strftime("%H:%M")
        df.elapsed = df.elapsed[df.elapsed.notnull()].astype(int).apply(str)
        df.remaining = df.remaining[df.remaining.notnull()].astype(int).apply(str)
        df = df[cols].fillna("").sort_values("started", ascending=False)
        return df
