# Lemmings

`lemmings` is an small yet powerful load testing tool. 
It is intended for load-testing (web-)systems by test scenarios written in asynchronous way.


## Features
* **test steps written as async method**<br>
* **system-independent**<br>
 In most cases tests written in **lemmings** are web-oriented, but it is possible to test almost any system. 

* **load generation' metrics**<br>
 Each worker produce **Prometheus**-ready metrics. <br>
 It is possible either to pull current metrics from worker or push metrics to **Influx**.

## Quick start 

1. 'pip install lemmings'

'''
class TargetsTestPlan(BaseTestPlan):

    @Task(weight=5)
    async def test_create_target(self, run):
        await self.service.create_entity(1, "test")

    @Task(weight=3)
    async def test_wait(self, run):
        await run.sleep(self.timings.wait_time, "do nothing during wait time")
        await self.service.remove_entity(1)

'''

## How it works

TODO

## Shared data 

Each test suite is executing by pool of workers in parallel. Each worker run in diffent process with `multiprocessing`
<br>
It is possible to use shared variable using standard `multiprocessing` features (Lock, Array, Value, manager, etc.)
<br> 
TODO

## License

Open source licensed under the MIT license (see _LICENSE_ file for details).

## Supported Python Versions

Locust is supported on Python >=3.7