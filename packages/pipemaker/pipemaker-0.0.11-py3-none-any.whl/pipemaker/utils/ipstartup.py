"""
setup jupyter for data analysis. 
"""
from .defaultlog import log, getlog
import logging
import warnings

if log.getEffectiveLevel() > logging.DEBUG:
    warnings.filterwarnings("ignore")


def flog(text):
    """ for finding logging problems """
    with open("c:/flog.txt", "a") as f:
        f.write(str(text))


def resetlog():
    global log
    log = getlog()


################## extensions ################################
try:
    get_ipython().magic("load_ext autoreload")
except:
    log.exception("")
try:
    get_ipython().magic("autoreload 2")  # autoreload all modules
except:
    log.exception("")
try:
    get_ipython().magic("matplotlib inline")  # show charts inline
except:
    log.exception("")
try:
    get_ipython().magic("load_ext cellevents")  # show time and alert
except:
    log.exception("")

################## common ################################
import os
import sys
from os.path import join, expanduser

################## analysis ################################
import pandas as pd
import numpy as np

from IPython.display import display as d
from IPython.core.display import HTML


def wide():
    """ makes notebook fill screen width """
    d(HTML("<style>.container { width:100% !important; }</style>"))
