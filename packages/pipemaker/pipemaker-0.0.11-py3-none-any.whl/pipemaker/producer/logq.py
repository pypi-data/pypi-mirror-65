#!/usr/bin/env python
from . import Rabbitq


class Logq(Rabbitq):
    """ logging queue """

    def __init__(self):
        super().__init__()
        self.queue = self.channel.queue_declare(queue=self.name, auto_delete=True)
