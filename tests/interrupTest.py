import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import weaklight
import threading
import time
import inspect

class Interrupt(threading.Thread, weaklight.core.threads.InterruptMixin):
    pass

def runner():
    time = 0.0
    loops = 0
    while True:
        print("{} loops in {}".format(loops, time), end='\r')
        loops +=1

def test():
    thread = Interrupt(target=runner)
    thread.daemon=True
    thread.start()
    time.sleep(1)
    thread.interrupt()

if __name__ == "__main__":
    test()
    print()