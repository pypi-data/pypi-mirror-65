"""
This is the core file to import into any notebook or program to create a pipeline.
It is only needed for the master not for the workers
"""
from .master.pipeline import pipeline
from .master.multiprocess import start, stop, kill, cleanup
from .filesystem import Filepath, Fpath
