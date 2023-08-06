import asyncio
import functools
import os
import time

from copy import copy
from prometheus_client import *
from prometheus_client.registry import REGISTRY

start = time.time()


class Timer():
    def __init__(self, name,
                 _text="{}# {}. Elapsed time: {:0.4f} seconds", _logger=print,
                 _prometheus=None, **labels):
        self.name = name
        self._text = _text
        self._logger = _logger

        self.labels = labels
        self.labels["process"] = os.getpid()
        self.labels["process_group"] = os.getppid()

        if _prometheus:  # clone
            self._count, self._failed, self._latency, self._in_progress = _prometheus
        else:
            self._count = Counter(f'operations_{self.name}_count', f'Total count for timer', self.labels)
            self._failed = Counter(f'operations_{self.name}_failed', f'Total failed for timer', self.labels)
            self._latency = Histogram(f'operations_{self.name}_latency', f'Latency for timer', self.labels)
            self._in_progress = Gauge(f'operations_{self.name}_in_progress', f'Operations in progress', self.labels)

    def text(self, _text):
        self._text = _text
        return self

    def logger(self, _logger):
        self._logger = _logger
        return self

    @property
    def start(self):
        return self._start_time

    @property
    def elapsed(self):
        return time.perf_counter() - self._start_time

    # use timer object as context manager ('with' syntax)
    def __enter__(self):
        self._start_time = time.perf_counter()
        self._in_progress.labels(**self.labels).inc()
        return self

    def __exit__(self, type, value, traceback):
        global start
        if self._in_progress:
            self._in_progress.labels(**self.labels).dec()
        if self._failed:
            if isinstance(value, BaseException):
                self._failed.labels(**self.labels).inc()
        if self._count:
            self._count.labels(**self.labels).inc()
        if self._latency:
            self._latency.labels(**self.labels).observe(self.elapsed)
        if self.logger and self.name:
            self.logger(self._text.format(self.name, time.time() - start, self.elapsed))

    # use object as decorator
    def __call__(self, func=None, **kwargs):
        if not func:
            registered = set(self.labels.keys()) - {'process', 'process_group'}
            overridden = dict(self.labels)
            for k, v in kwargs.items():
                if not k in registered:
                    raise Exception(f"invalid labels for timer: {kwargs.keys()} [should be from {registered}")
                overridden[k] = v
            return Timer(self.name, self._text, self._logger,
                         (self._count, self._failed, self._latency, self._in_progress),
                         # shouldn't override prometheus metrics
                         **overridden)
        else:
            # use object as decorator
            if asyncio.iscoroutinefunction(func):
                @functools.wraps(func)
                async def wrapper_timer(*args, **kwargs):
                    with copy(self) as timer:
                        # with self as timer:
                        timer._text += " [{}]".format(args)
                        return await func(*args, **kwargs)

                return wrapper_timer
            else:
                @functools.wraps(func)
                def wrapper_timer(*args, **kwargs):
                    with copy(self) as timer:
                        timer._text += " [{}]".format(args)
                        return func(*args, **kwargs)

                return wrapper_timer

    def __str__(self):
        return self.name


if __name__ == '__main__':
    @Timer("testA", label11="value11", label12="value12")
    def a(text):
        print(f"run a('{text}')")
        time.sleep(1)


    timer = Timer("testB", label21="a", label22="c")


    def b(text):
        with timer(label21="value21"):
            print(f"run b('{text}')")
            time.sleep(1)


    a("start11")
    a("start12")
    b("start21")
    b("start22")
    b("start23")

    # influx = Influx(REGISTRY)
    # print(influx.save("count", "sum"))
