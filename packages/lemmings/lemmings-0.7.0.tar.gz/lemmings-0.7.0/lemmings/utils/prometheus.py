import os
import shutil

from prometheus_client import CollectorRegistry, multiprocess

from lemmings.utils.influx import Influx


class Prometheus:
    def __init__(self, shared_dir='./prometheus.tmp'):
        self.path = os.environ.setdefault('prometheus_multiproc_dir', shared_dir)
        shutil.rmtree(self.path, ignore_errors=True)
        os.mkdir(self.path)

        self.registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(self.registry)
        self.influx = Influx(self.registry)

    def filter(self, *args):
        self.args = args

    def dump_to_influx(self):
        print(self.influx.save(*self.args))

    def clean(self):
        try:
            shutil.rmtree(self.path)
            print("temporary prometheus dir cleared")
        except BaseException as e:
            print("problem with temporary prometheus dir: ", e)
