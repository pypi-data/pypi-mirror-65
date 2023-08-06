#!/usr/bin/env python
from .rabbitq import Rabbitq
from threading import Thread
import functools

import logging

log = logging.getLogger(__name__)


class Workerq(Rabbitq):
    """ a task queue that executes one task at a time in a thread """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = self.channel.queue_declare(queue=self.name, auto_delete=True)
        self.channel.basic_qos(prefetch_count=1)

    def handle_message(self, method, body):
        """ execute task in separate thread to listener """

        def target(delivery_tag, body):
            body.run()
            cb = functools.partial(self.ack_message, delivery_tag)
            self.connection.add_callback_threadsafe(cb)

        t = Thread(target=target, args=(method.delivery_tag, body), daemon=True)
        t.start()
