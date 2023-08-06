import pika
import dill as pickle
import multiprocess as mp
import logging

log = logging.getLogger(__name__)


class Rabbitq:
    """ base class for a consumer

    rabbitmq has these benefits versus python queue managers:
    * resilience to queue failure via persistence, distributed deployment
    * resilience to consumer or network failure via message acknowledgements; heartbeats
    * flexible routing
    * tools for monitoring consumer
    * ability to handle high volumes of messages simultaneously
    * push consumer rather than polling
    * communication with non-python applications
    * everything on a single port. python multiprocess managers each have a port.
    """

    STOP = "STOP_CONSUMING"

    def __init__(self, heartbeat=60):
        """ create channel but not a queue
        :param heartbeat: consumer typically 60.
        """
        params = pika.connection.ConnectionParameters(heartbeat=heartbeat)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.name = self.__class__.__name__

    @classmethod
    def start_consuming_process(cls, name="", **kwargs):
        """ listen to a queue in a background process
        class method to avoid pickling issues
        """

        def target(cls, **kwargs):
            from ..utils.defaultlog import logging

            log = logging.getLogger(__name__)

            heartbeat = kwargs.pop("heartbeat", 60)
            queue = cls(heartbeat=heartbeat)
            queue.listen()

        p = mp.Process(target=target, args=(cls,), kwargs=kwargs, name=name)
        p.start()

    def listen(self):
        """ blocking loop that makes callback for each message received
        """
        self.channel.basic_consume(queue=self.name, on_message_callback=self.callback)
        name = f"{self.name} {mp.current_process().name}"
        log.info(f"start consuming {name}")
        try:
            self.channel.start_consuming()
            log.info(f"stop consuming {name}")
        except KeyboardInterrupt:
            log.info(f"keyboard interrupt. stop consuming {name}")
        except:
            log.exception(f"consumer failed {name}")
        finally:
            self.channel.close()

    def callback(self, ch, method, properties, body):
        """ callback when message received from listen """
        try:
            body = self.decode(body)
            if body == self.STOP:
                self.channel.stop_consuming()
                return
            self.handle_message(method, body)
        except:
            log.exception(f"{self.name} unable to handle message={body}")

    def handle_message(self, method, body):
        """ override this to handle decoded message """
        raise NotImplementedError(
            f"override handle_message to handle messages for {self.name}"
        )

    def decode(self, body):
        """ message to object """
        return pickle.loads(body)

    def ack_message(self, delivery_tag):
        if self.channel.is_open:
            self.channel.basic_ack(delivery_tag)

    def list(self, limit=20):
        """ return list of messages without removing from queue """
        messages = []
        tags = []
        while True:
            method, prop, body = self.channel.basic_get(self.queue.method.queue)
            if method is None:
                break
            messages.append(self.decode(body))
            tags.append(method.delivery_tag)
            if len(messages) >= limit:
                log.warning(
                    f"Returning {limit} messages. Increase limit parameter to get more"
                )
                break
        # requeue
        for tag in tags:
            self.channel.basic_nack(delivery_tag=tag)
        return messages

    def pop(self):
        """ return one item from queue and remove from queue """
        r = self.channel.basic_get(self.name, auto_ack=True)
        if r[-1]:
            return self.decode(r[-1])
        else:
            return None
