import traceback
import sys

class Maybe(object):
    def __init__(self, value=None, tb=None, tb_class=None, e=None):
        self.value = value
        self.trace = tb
        self.e = e
        self.trace_class = tb_class

    def __repr__(self):
        if self.is_exception():
            return "{}({})".format(self.__class__.__name__, self.trace_class)
        else:
            return "{}({}({}))".format(self.__class__.__name__, type(self.value), self.value.__repr__())

    def is_exception(self):
        """
        Returns a boolean, if the value contains an exception
        """
        return self.e != None

    def get_traceback(self):
        """
        Returns a traceback.TracebackException
        """
        return self.trace

    def get_exception(self):
        """
        Returns the exception class or None
        """
        return self.trace_class

    def get(self):
        """
        Returns either the captured value, or raises the exception
        """
        if not self.is_exception():
            return self.value
        else:
            raise self.e

def wrap(func, *args, **kwargs):
    """
    Convert a function call into a Maybe
    """
    try:
        val = func(*args, **kwargs)
        exc = None
        tb = None
        tb_class = None
    except Exception as e:
        exc = e
        val = None

        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.TracebackException(exc_type, exc_value, exc_traceback)
        tb_class = exc_type

    r = Maybe(val, tb, tb_class, exc)
    return r

def decorate(func):
    """
    Make sure a function returns a Maybe
    """
    def wrapper(*args, **kwargs):
        try:
            val = func(*args, **kwargs)
            exc = None
            tb = None
            tb_class = None
        except Exception as e:
            exc = e
            val = None

            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.TracebackException(exc_type, exc_value, exc_traceback)
            tb_class = exc_type

        r = Maybe(val, tb, tb_class, exc)
        return r
    return wrapper
