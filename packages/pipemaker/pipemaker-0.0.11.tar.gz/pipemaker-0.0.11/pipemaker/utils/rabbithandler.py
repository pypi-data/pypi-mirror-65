from ..producer import Logq
import logging


class RabbitHandler(logging.Handler):
    """ logging handler that outputs to rabbit queue
    """

    def __init__(self):
        super().__init__()
        self.q = Logq()

    def emit(self, record):
        """ log the record """
        msg = self.format(record)
        self.q.put(msg)
