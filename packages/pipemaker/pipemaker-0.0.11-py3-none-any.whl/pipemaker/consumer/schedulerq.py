from . import Rabbitq
from ..producer import Workerq, Responseq
import logging

log = logging.getLogger(__name__)


class Schedulerq(Rabbitq):
    """ queue that schedules new tasks; and responds to events from existing tasks
    """

    # dict(url=task) of submitted tasks including waiting, running, completed, failed
    tasks = dict()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queue = self.channel.queue_declare(queue=self.name, auto_delete=True)
        self.worker = Workerq()

    def handle_message(self, method, body):
        """ pass event to handler
        :param body: dict with time, event, process, output
        """
        try:
            getattr(self, body["event"])(body)
        except:
            log.exception(f"Error processing event {body}")
        finally:
            self.ack_message(delivery_tag=method.delivery_tag)

    # handlers ####################################################

    def onRun(self, body):
        """ new tasks arrive here as dict(url=task) including upstream tasks """
        for k, v in body["tasks"].items():
            # if already scheduled then just add in the new downstream task
            current = self.tasks.get(k)
            if current:
                current.downstream = current.downstream | (v.downstream)
                continue
            v.status = "waiting"
            self.tasks[k] = v
            if not v.upstream:
                v.status = "ready"
                self.worker.put(v.workertask)

    def onRunning(self, body):
        """ finished loading data and started processing """
        task = self.tasks[body["source"]]
        task.status = "running"
        task.process = body["process"]
        task.started = body["time"]
        task.finished = None

    def onProgress(self, body):
        """ handles event fired by task to show progress """
        task = self.tasks[body["source"]]
        task.progress = int(body["progress"])

    def onComplete(self, body):
        """ task has completed and all output has been written """

        # update the task on data and release any downstream
        task = self.tasks[body["source"]]
        task.status = "completed"
        task.finished = body["time"]
        task.progress = 100
        task.details = ""

        # run any tasks that can now run
        for d in task.downstream:
            dtask = self.tasks[d]
            dtask.upstream.remove(task.url)
            if not dtask.upstream:
                dtask.status = "ready"
                self.worker.put(dtask.workertask)
        task.downstream = set()

        # notify complete if there are consumers already but don't wait.
        Responseq(task.url).put()

    def onError(self, body):
        task = self.tasks[body["source"]]
        task.status = "failed"
        task.details = str(body["exception"])
        self.fail_downstream(task)

    def fail_downstream(self, task):
        """ recursively fail all downstream tasks """
        for d in task.downstream:
            dtask = self.tasks[d]
            dtask.status = "failed_upstream"
            dtask.details = str(task)
            self.fail_downstream(dtask)

    def onLoading(self, body):
        """ task has been received by a workertask and is loading the data before processing """
        task = self.tasks[body["source"]]
        task.status = "loading"

    def onSaving(self, body):
        """ task has finished and output is being saved """
        task = self.tasks[body["source"]]
        task.status = "saving"

    def onView(self, body):
        """ sends unformatted copy of the task queue to body queue
        :body: dict(key=routing_key). caller uses routing key to match request/body.
        """
        key = body["key"]
        Responseq(key).put(self.tasks)
