#!python
import subprocess
import os

PROJECT = os.path.abspath(os.path.join(os.pardir, os.path.dirname(__file__)))
HOME = "/home/root"

# remove old container
cmd = "docker rm -f pm"
subprocess.run(cmd, capture_output=True)

# map data, scripts, source; pipe; jupyter port
cmd = (
    "docker run --name pm "
    f" -v {PROJECT}/scripts/pipedata:{HOME}/scripts/pipedata"
    f" -v {PROJECT}/scripts:{HOME}/scripts"
    f" -v {PROJECT}/pipemaker:{HOME}/pipemaker"
    f" -v {PROJECT}/.jupyter:{HOME}/.jupyter"
    f" --hostname pm "
    " -p 8890:8888"
    " -d"
    " pm"
)

# launch
subprocess.run(cmd)
