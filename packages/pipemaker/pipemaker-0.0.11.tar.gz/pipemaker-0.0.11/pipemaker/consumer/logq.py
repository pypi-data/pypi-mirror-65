#!/usr/bin/env python
from pipemaker.consumer import Rabbitq
import os

PATH = os.path.dirname(__file__)


class Logq(Rabbitq):
    """ logging queue that writes to log file
    """

    def __init__(self, filename=f"{PATH}/log.txt", **kwargs):
        super().__init__(**kwargs)
        # exclusive. one consumer writes to file
        self.queue = self.channel.queue_declare(queue=self.name, auto_delete=True)
        self.logfile = open(filename, "w")

    def listen(self):
        super().listen()
        self.logfile.close()

    def handle_message(self, method, body):
        self.logfile.write(body)
        self.logfile.write("\n")
        self.logfile.flush()
        self.ack_message(method.delivery_tag)


if __name__ == "__main__":
    # entry point log setup
    from defaultlog import log

    logq = Logq()
    logq.listen()
