from threading import Thread
from types import FunctionType
from typing import List
import time

def setInterval(f: FunctionType, args: List, interval: int):
    """
    Execute function f with args in every interval seconds
    """
    def helper():
        while True:
            f(*args)
            time.sleep(interval)
    # start a thread to execute helper function
    Thread(target=helper, args=tuple(args)).start()
