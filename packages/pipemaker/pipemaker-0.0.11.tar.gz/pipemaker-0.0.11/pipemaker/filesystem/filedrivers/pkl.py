import pickle
import logging

log = logging.getLogger(__name__)


def save(self, obj, fpath):
    """ save a pickle file """
    pickle.dump(obj, fpath.open("wb"))


def load(self):
    """ load a pickle file """
    return pickle.load(self.open("rb"))
