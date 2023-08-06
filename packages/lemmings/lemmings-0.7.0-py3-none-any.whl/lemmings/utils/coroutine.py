import asyncio
import concurrent
import functools
import time
from datetime import timedelta

from lemmings.utils.parsing import parse_duration


def duration2sec(duration):
    """
    convert duration to seconds (as float)
    :param duration: seconds, timedelta or formatted string
    :return:
    """
    if isinstance(duration, str):
        duration = parse_duration(duration)
    if isinstance(duration, timedelta):
        duration = duration.total_seconds()
    return duration


def async_timeout(duration):
    """
    timeout decorator for async function
    :param duration:
    :return:
    """

    def wrap(func):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper_timer(*args, **kwargs):
                start = time.time()
                try:
                    return await asyncio.wait_for(func(*args, **kwargs), duration2sec(duration))
                except concurrent.futures._base.TimeoutError as e:
                    actual = timedelta(seconds=time.time() - start)
                    print(f"timeout during {func.__name__}({args}) [after: {actual}, max: {duration}]")
                    return None
            return wrapper_timer
    return wrap


def in_thread_executor(f):
    """
    Convert func to async: run sync code in thread executor
    WARNING! Code could not be cancelled by async helpers
    :param f:
    :return:
    """

    @functools.wraps(f)
    async def wrap(*args):
        ts = time.time()
        # None uses the default executor (ThreadPoolExecutor)
        result = await asyncio.get_event_loop().run_in_executor(None, f, *args)
        te = time.time()
        print('* %s tooks: %2.4f sec. \n - args: %r' % (f.__name__.upper(), te - ts, args))
        return result

    return wrap
