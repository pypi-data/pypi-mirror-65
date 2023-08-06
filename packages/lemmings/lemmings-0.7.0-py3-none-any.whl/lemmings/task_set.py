import datetime

from lemmings import Task


class TaskSetMeta(type):
    def __new__(cls, className, bases, classDict):
        tasks = TaskSetMeta.inhereted_tasks(bases)
        for name, item in classDict.items():
            if isinstance(item, Task):
                item.set_name(name)
                tasks.append(item)
        classDict["tasks"] = tasks
        return type.__new__(cls, className, bases, classDict)

    @staticmethod
    def inhereted_tasks(bases):
        tasks = []
        for base in bases:
            if hasattr(base, "tasks") and isinstance(base.tasks, list):
                tasks += base.tasks
        return tasks


class TaskSet(object, metaclass=TaskSetMeta):
    tasks = []

    def __init__(self):
        self.is_sequence = self._is_sequence()
        self.duration = None
        self.runs = len(self.tasks)
        self.sleep_time = datetime.timedelta(0)
    def max_runs(self, max_run):
        self.runs = max_run
        return self
    def max_duration(self, duration):
        self.duration = duration
        return self
    def rps(self, rps):
        self.sleep_time = datetime.timedelta(seconds=1/rps)
        return self

    # for override in task sets
    async def setup(self, task_set, run):
        pass
    async def teardown(self, task_set, run):
        pass

    def _is_sequence(self):
        ordered = 0
        for item in self.tasks:
            if item.order > 0:
                ordered += 1
        if ordered > 0:
            if ordered != len(self.tasks):
                print(f"WARNING! Found only {ordered} ordered task(s) from {len(self.tasks)} total")
                print("To run tasks as sequence, all tasks should be ordered")
            else:
                return True
        return False

    @property
    def weight_total(self):
        i = 0
        for t in self.tasks:
            i += t.weight
        return i

    def __str__(self):
        return f"{self.__class__.__name__} [{self.runs}, {self.duration}]: {', '.join(map(str, self.tasks))} [total: {self.weight_total}]"

