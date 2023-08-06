import asyncio
import datetime
import os
import sys
import time
import traceback
from asyncio.locks import BoundedSemaphore

from lemmings.task_set_run import TaskSetRun
from lemmings.utils import _num, duration2sec
from lemmings.utils.colors import Color
from lemmings.utils.const import DONE, FAIL

program_start = time.time()


class Worker:
    total = 0

    def __init__(self, name, task_set, max_in_parallel=1000, debug=False):
        Worker.total += 1
        self.debug = debug
        self.id = Worker.total
        self.name = name
        self.task_set = task_set

        self.title = f"{self.name}[{self.id}]"
        self.max_in_parallel = max_in_parallel

        # will be init in execute (in child processes):
        self.stat = None
        self.shared_state = None
        self.semaphore = None

    def set_title(self, title):
        self.title = title

    def set_shared(self, shared_state):
        self.shared_state = shared_state

    def set_statistics(self, stat):
        self.stat = stat

    async def run_task(self, offset, task):
        await asyncio.sleep(duration2sec(offset))
        start = time.time()

        def print_stat(prefix, print=True, comment="", success=False, failed=False):
            succ = Color.mark(Color.green, _num(self.stat.executed))
            fail = Color.mark(Color.red, _num(self.stat.failed))
            if success:
                succ = Color.bold(succ)
            if failed:
                fail = Color.bold(fail)
            total = _num(self.stat.total)
            if task.comment:
                comment = task.comment + " " + comment
            if print:
                self.log(f"{prefix:5}> {succ} / {fail} / {total} in {time.time() - start:.2f} sec", comment)

        try:
            async with self.semaphore:
                print_stat("Run  ", self.debug)
                await task.__call__(task)(self.task_set, self.task_run)
                if not task.system:
                    self.stat.success()
                print_stat(DONE, success=True)
        except BaseException as e:
            if not task.system:
                self.stat.fail()
            print_stat(FAIL, comment=str(e), failed=True)
            if self.debug:
                print(e)
                traceback.print_stack(file=sys.stdout)

    def execute(self):
        loop = asyncio.get_event_loop()
        offset = datetime.timedelta(0)
        scheduled_tasks = []

        def schedule(task):
            nonlocal offset
            future = asyncio.ensure_future(self.run_task(offset, task))
            scheduled_tasks.append(future)
            if not task.system:
                self.stat.schedule()
                offset += self.task_set.sleep_time

        self.task_run = TaskSetRun(self, self.task_set)
        self.semaphore = self._semaphore()

        # setup
        schedule(self.task_run.setup_task())

        for task in self.task_run:
            schedule(task)
        self.log(f"Queue: {_num(self.stat.total)} in worker / {_num(self.stat.shared_total)} total")
        loop.run_until_complete(asyncio.wait(scheduled_tasks))

        # teardown
        scheduled_tasks = []
        schedule(self.task_run.teardown_task())
        loop.run_until_complete(asyncio.wait(scheduled_tasks))

        self.dump_results()
        return os.getpid()

    def _semaphore(self):
        p = self.max_in_parallel
        if self.task_run.is_ordered:  # no concurrent run in ordered execution
            p = 1
        return BoundedSemaphore(p)

    def dump_results(self):
        with self.stat.lock:
            self.log(f"worker results: {_num(self.stat.executed)} {DONE},"
                     f" {_num(self.stat.failed)} {FAIL} "
                     f"[{_num(self.stat.total)} total]")
            self.log(f"total  results: {_num(self.stat.shared_executed)} {DONE},"
                     f" {_num(self.stat.shared_failed)} {FAIL} "
                     f"[{_num(self.stat.shared_total)} total]")

    def log(self, msg, comment=""):
        global program_start
        if comment:
            comment = " | " + Color.cursive(comment)
        Color.print(self.id, f'{self}', f" {msg} {comment}", prefix=f"| {(time.time() - program_start):7.3f} ")

    def __str__(self):
        return self.title
