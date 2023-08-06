import asyncio
import collections
import random
import time
from datetime import timedelta

from lemmings.task import Task
from lemmings.utils.coroutine import duration2sec


class TaskSetRun:
    def __init__(self, worker, task_set):
        self.worker = worker
        self.task_set = task_set
        self.total = len(self.task_set.tasks)

        self.current = -1  # idx in task_set of current task (for generator)
        self.generated = 0  # current count of generated tasks
        for item in self.task_set.tasks:
            item.set_test_plan(task_set)
        self.start_time = time.time()

    @property
    def shared(self):
        return self.worker.shared_state

    def log(self, msg, comment=""):
        self.worker.log(msg, comment)

    async def sleep(self, duration=None, comment=""):
        if not duration:
            duration = timedelta(seconds=random.random())
        if duration.total_seconds() > 3:
            self.log(f"SLEEP FOR {duration}", comment)
        await asyncio.sleep(duration2sec(duration))

    async def in_duration(self, duration, times) -> collections.AsyncIterable:
        start_time = time.time()
        for step in range(times):
            yield step
            elapsed = timedelta(seconds=time.time() - start_time)
            if times - step > 1:
                sleep_time = (duration - elapsed) / (times - step - 1)
                await self.sleep(sleep_time, f"after #{step + 1} step of {times} total in duration {duration}")

    def rps_in_duration(self, duration, rps) -> collections.AsyncIterable:
        return self.in_duration(duration, duration * rps)

    def with_rps(self, rps):
        class RPS:
            def __init__(self, rps, runner):
                self.rps = rps
                self.runner = runner

            def in_duration(self, duration, rps) -> collections.AsyncIterable:
                return self.runner.in_duration(duration, duration * rps)

        return RPS(rps, self)

    @property
    def is_ordered(self):
        return self.task_set.is_sequence

    @property
    def tasks(self):
        return self.task_set.tasks

    @property
    def sorted_tasks(self):
        return sorted(self.tasks, key=lambda t: t.order)

    def setup_task(self):
        return Task(self.task_set.setup, system=True, comment="Setup * ")

    def teardown_task(self):
        return Task(self.task_set.teardown, system=True, comment="Teardown * ")

    def __iter__(self):
        return self

    def __next__(self):
        # timeout by TaskSet's 'max_duration' parameter
        if self.task_set.duration is not None:
            if time.time() - self.start_time >= self.task_set.duration.total_seconds():
                raise StopIteration
        # stop by TaskSet's 'max_run' parameter
        if self.generated > self.task_set.runs:
            raise StopIteration
        if self.is_ordered:
            s = self.ordered()
            if s is None:
                raise StopIteration
            return s
        else:
            return self.weighted_random()

    def _schedule_teardown(self):
        self.in_processing = False
        return Task(self.task_set.teardown, system=True, comment="Teardown * ")

    def weighted_random(self):
        n = random.uniform(0, self.task_set.weight_total)
        for idx, item in enumerate(self.tasks):
            if n < item.weight:
                self.current = idx
                self.generated += 1
                return item
            n = n - item.weight
        return None

    def ordered(self):
        self.current += 1
        if self.current >= self.total:
            return None
        self.generated += 1
        return self.sorted_tasks[self.current]
