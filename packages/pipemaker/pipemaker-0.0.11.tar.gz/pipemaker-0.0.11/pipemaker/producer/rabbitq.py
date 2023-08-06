import pika
import dill as pickle
import logging

log = logging.getLogger(__name__)


class Rabbitq:
    """ base class for a producer """

    def __init__(self, heartbeat=0):
        """
        :param heartbeat: producer=0 unless frequent messages
        """
        params = pika.connection.ConnectionParameters(heartbeat=heartbeat)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.name = self.__class__.__name__

    def put(self, body="", **kwargs):
        """ put a message on the queue
        :param body: message to send
        """
        body = self.encode(body)
        kwargs.setdefault("exchange", "")
        kwargs.setdefault("routing_key", self.name)
        self.channel.basic_publish(body=body, **kwargs)

    def encode(self, body):
        """ object to message """
        return pickle.dumps(body)
