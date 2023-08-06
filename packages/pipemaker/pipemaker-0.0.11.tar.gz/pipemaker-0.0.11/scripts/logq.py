#!python
from pipemaker.consumer.logq import Logq

print("listening for log messages", flush=True)
Logq().listen()
