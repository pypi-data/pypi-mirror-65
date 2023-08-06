from multiprocessing import Lock

from lemmings.shared import SharedValue


class Statistics:
    def __init__(self):
        self.lock = Lock()
        self.processed = 0
        self.executed = 0
        self.failed = 0
        self.total = 0
        self.shared_executed = SharedValue(0)
        self.shared_failed = SharedValue(0)
        self.shared_total = SharedValue(0)  # .with_name("total") # debug

    def schedule(self):
        self.total += 1
        self.shared_total += 1

    def success(self):
        self.processed += 1
        self.executed += 1
        self.shared_executed += 1

    def fail(self):
        self.processed += 1
        self.failed += 1
        self.shared_failed += 1
