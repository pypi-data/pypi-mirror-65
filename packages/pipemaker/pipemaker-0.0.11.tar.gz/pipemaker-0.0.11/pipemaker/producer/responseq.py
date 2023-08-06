from .rabbitq import Rabbitq
import logging

log = logging.getLogger(__name__)


class Responseq(Rabbitq):
    """ queue for each key

    Applications::
    * To wait for an event to happen. can be called by multiple consumers.
    * To request data from a queue and wait for response
    """

    def __init__(self, key):
        """
        :param key: unique routing key e.g name of file OR random string
        """
        super().__init__()

        # ttl enables producer to generate message before consumer has started
        # expires deletes queue if no consumers
        self.queue = self.channel.queue_declare(
            queue=key, arguments={"x-message-ttl": 500, "x-expires": 1000}
        )
        self.key = key

    def put(self, body=None):
        """ send response to all consumers
        :param body: optional response data
        """
        super().put(body, routing_key=self.key)
        self.connection.close()
