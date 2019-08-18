import threading
from . import exceptions
import inspect
import ctypes

def _async_raise(tid, exctype):
    '''
    This method interruprs a thread to stop it mid execution.  
    '''
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class InterruptMixin(object):
    '''
    This is a mixin for a thread to allow it to be interruped
    '''
    def _get_my_tid(self):
        if not self.isAlive():
            raise threading.ThreadError("The thread is not active")
        
        if hasattr(self, "_thread_id"):
            return self._thread_id
        
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid
        
        raise AssertionError("Could not determine the thread's id")
    
    def interrupt(self):
        """raises SystemExit in the context of the given thread, which should 
        cause the thread to exit silently (unless caught)"""
        _async_raise(self._get_my_tid(),exceptions.Interrupted)