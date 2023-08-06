from .comm import SerialPort
from .comm import mlink
from .boards import *

import sys
import signal

_ports = []
_threads = []

def add_port(port):
    global _ports
    _ports.append(port)

def add_thread(thread):
    global _threads
    _threads.append(thread)

def __exiting(signal, frame):
    global _ports
    global _threads
    for port in _ports:
        port.exit()
    for thread in _threads:
        thread.exit()
    sys.exit(0)

signal.signal(signal.SIGINT, __exiting)

