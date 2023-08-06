## Lemmings

`lemmings` is an small yet powerful load testing tool. 
It is intended for load testing of (web-)systems by test scenarios written in asynchronous way.


### Features
* test steps written as async method<br>
* system-independent<br>
 In most cases tests written in `lemmings` are web-oriented, but it is possible to test almost any system if there is async way to communicate with it. 
* metrics for generator  performance <br>
 Each running worker produce **Prometheus**-ready metrics. <br>
 It is possible either to pull current metrics from worker or push metrics to **Influx**.

## Quick start 

1. Install library (Python >=3.7 required) <br> 
`pip install lemmings`

2. Create test suite 
```python
from lemmings import *

class ExampleTestPlan(TaskSet):

    @Task(weight=5)
    async def test_create_target(self, run):
        await self.service.create_entity(1, "test")

    @Task(weight=3)
    async def test_wait(self, run):
        await run.sleep(self.timings.wait_time, "do nothing during wait time")
        await self.service.remove_entity(1)

```
2. Create test suite 
```python
import multiprocessing
from lemmings import *
if __name__ == '__main__':
        prometheus = Prometheus()
        
        shared = multiprocessing.Value("i", 0)

        g = TestExecutor()
        g.add_test_plan(ExampleTestPlan())

        g.start_all(shared)

        prometheus.dump_to_influx()
        prometheus.clean() # workaround against prometheus work with multiprocessing

```

## How it works

**TODO**

## Shared data 

Each test suite is executing by pool of workers in parallel. Each worker run in diffent process with `multiprocessing`
<br>
It is possible to use shared variable using standard `multiprocessing` features (Lock, Array, Value, manager, etc.)
<br> 

**TODO**

## License

Open source licensed under the MIT license (see _LICENSE_ file for details).

## Supported Python Versions

Locust is supported on Python >=3.7