import asyncio
import functools

from lemmings.utils.timer import Timer


class Task:
    DEFAULT = Timer("default")

    def __init__(self, func=None, weight=1, order=0, comment="", system=False):
        self.name = "noname"
        self.timer = Task.DEFAULT
        self.func = func
        self.weight = weight
        self.order = order
        self.comment = comment
        self.system = system

    def set_name(self, name):
        self.name = name

    def set_test_plan(self, test_plan):
        self.test_plan = test_plan
        if (self.timer.name == "default") and (self.name != "noname"):
            self.timer = Timer(f"{self.test_plan.__class__.__name__}_{self.name}".lower())

    # use object as decorator
    def __call__(self, func=None):
        if not callable(self.func):  # no arguments to decorator (only @Task)
            self.func = func
            return self
        if asyncio.iscoroutinefunction(self.func):
            @functools.wraps(self.func)
            async def wrapper_timer(*args, **kwargs):
                with self.timer:
                    with self:
                        return await self.func(*args, **kwargs)

            return wrapper_timer
        else:
            @functools.wraps(self.func)
            def wrapper_timer(*args, **kwargs):
                with self.timer:
                    with self:
                        return self.func(*args, **kwargs)()

            return wrapper_timer

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        # if isinstance(value, BaseException):
        #     print(f"exception during {self.name}: {value}")
        # return isinstance(value, TypeError)
        return

    def __str__(self):
        return f"{self.name}[w={self.weight}]"
