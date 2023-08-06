from .rabbitq import Rabbitq
import logging

log = logging.getLogger(__name__)


class Responseq(Rabbitq):
    """ default exchange. queue created for each key.

    Applications::
    * To wait for an event to happen. can be called by multiple consumers.
    * To request data from a queue (provide key) and wait for response on key.
    """

    def __init__(self, key, *args, **kwargs):
        """
        :param key: unique routing key e.g name of file OR random string
        """
        super().__init__(*args, **kwargs)

        # ttl enables producer to generate message before consumer has started
        # expires deletes queue if no consumers
        self.queue = self.channel.queue_declare(
            queue=key, arguments={"x-message-ttl": 500, "x-expires": 1000}
        )

    def listen(self, **kwargs):
        """ listen for one event; stop; return response
        :param timeout: if exceeded then call callback_timeout
        """
        timeout = kwargs.pop("timeout", None)
        if timeout:
            self.connection.call_later(timeout, self.callback_timeout)
        self.channel.basic_consume(
            queue=self.queue.method.queue, on_message_callback=self.callback, **kwargs
        )
        self.channel.start_consuming()
        return self.response

    def callback(self, ch, method, properties, body):
        """ when message received then set response and stop """
        self.response = self.decode(body)
        self.channel.stop_consuming()
        self.connection.close()

    def callback_timeout(self):
        """ callback when timeout exceeded """
        raise TimeoutError()
