import functools
import inspect
import random
import sys
import traceback
from contextlib import contextmanager

from lemmings.utils.timer import Timer

timer = Timer("timed_execution", module="", clazz="unknown", method="unknown")


def random_by_weight(list, weight_func):
    weight_total = sum(weight_func(i) for i in list)
    n = random.uniform(0, weight_total)
    for idx, item in enumerate(list):
        if n < weight_func(item):
            return item
        n = n - weight_func(item)
    return None


def timed_execution(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        clazz = args[0].__class__.__name__ if is_method(f) else "unknown"
        with timer(module=f.__module__, clazz=clazz, method=f.__name__):
            return f(*args, **kwargs)

    return wrap


def ignore_exception(func):
    @functools.wraps(func)
    def function_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            print(e)

    return function_wrapper


def is_method(fn):
    try:
        return inspect.getfullargspec(fn)[0][0] == 'self'
    except:
        return False


@contextmanager
def debug(file=sys.stdout):
    try:
        yield file
    except BaseException as e:
        print(e)
        traceback.print_stack(file=file)
        raise
