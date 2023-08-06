#!python
import flask
import multiprocess as mp
import requests
from time import sleep
from IPython.core.display import HTML

from ..producer import Schedulerq

import logging

log = logging.getLogger(__name__)

app = flask.Flask(__name__)
server = None


@app.route("/shutdown")
def shutdown():
    """ shutdown flask from inside a request """
    func = flask.request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()
    return "Server shutting down"


@app.route("/")
def status():
    """ render html page with tables showing queues, task summary, tasks """
    tables = []
    titles = []

    # queues
    tables.append(queues())
    titles.append("Queues")

    # task summary
    status = [
        "waiting",
        "ready",
        "loading",
        "running",
        "saving",
        "completed",
        "failed",
        "failed_upstream",
        "total",
    ]
    df = Schedulerq().view()

    if df is None:
        titles.append("Tasks")
        tables.append("No tasks are scheduled")
    else:
        # task summary
        summary = df.groupby("status")[["url"]].count().T
        summary.columns.name = None
        for col in set(status) - set(summary.columns):
            summary[col] = 0
        summary = summary.fillna(0)
        summary["total"] = summary.sum(axis=1)
        tables.append(summary[status].to_html(index=False, table_id="summary"))
        titles.append("Task count by status")
        tables.append(df.to_html(table_id="task"))
        titles.append("Task list")

    return flask.render_template("view.html", tables=tables, titles=titles)


# control tasks  #########################################################################


def start():
    """ start flask in background process """

    def target():
        """ start flask process """
        from defaultlog import logging

        log = logging.getLogger(__name__)

        log.info(f"starting flask pid={mp.current_process().pid}")
        app.run(debug=False)

    global server
    if server:
        log.error("flask server already running")
        return
    log.info("starting server")
    server = mp.Process(target=target)
    server.start()


def stop():
    """ stop server. terminate process if available else send shutdown request
    """
    global server
    # terminate process
    if server:
        server.terminate()
        server.join()
        server = None
    # stop server via shutdown request
    else:
        log.info("sending shutdown request to flask server")
        try:
            r = requests.get("http://localhost:5000/shutdown")
            r.raise_for_status()
        except:
            return

        # wait
        while True:
            try:
                r = requests.get("http://localhost:5000")
                r.raise_for_status()
            except:
                break
            log.info("waiting for flask to shutdown")
            sleep(1)


def restart():
    """ restart server """
    stop()
    start()


def queues():
    """ display consumer in notebook """
    from ..consumer import Schedulerq, Workerq

    workerq = Workerq()
    schedulerq = Schedulerq()
    queues = [workerq, schedulerq]
    consumers = " ".join([f"{t.name}={t.queue.method.consumer_count}" for t in queues])
    messages = " ".join([f"{t.name}={t.queue.method.message_count}" for t in queues])

    return HTML(f"consumers: {consumers}<br>messages: {messages}<br>")


if __name__ == "__main__":
    """ for testing. normally run in background process """
    app.run(debug=True)
