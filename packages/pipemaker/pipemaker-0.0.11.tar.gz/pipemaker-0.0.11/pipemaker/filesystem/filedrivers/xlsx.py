from . import pandas


def save(self, obj, fpath):
    """ save pandas dataframe """
    pandas.save(self, obj, fpath, "to_excel")


def load(self):
    """ load pandas dataframe """
    return pandas.load(self, "read_excel")
