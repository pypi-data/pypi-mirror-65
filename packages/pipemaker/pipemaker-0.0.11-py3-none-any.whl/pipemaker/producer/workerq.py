#!/usr/bin/env python
from . import Rabbitq
import logging

log = logging.getLogger(__name__)


class Workerq(Rabbitq):
    """ default exchange with routing to class name  """

    pass
