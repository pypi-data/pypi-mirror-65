import asyncio
import inspect
import time

import pytest


@pytest.hookspec
def pytest_runtest_makereport(item, call):
    # Tests are run outside of the normal place, so we have to inject our timings
    if call.when == "call" and hasattr(item, "start"):
        call.start = item.start
        call.stop = item.stop


def not_coroutine_failure(*args, **kwargs):
    raise Exception("is not a coroutine. Add the async keyword to make it one")


async def test_wrapper(item):
    item.start = time.time()
    task = item.function()
    await task


@pytest.hookspec(firstresult=True)
def pytest_runtestloop(session):
    # Collect our coroutines
    item_by_coro = {}
    tasks = []
    for item in session.items:
        if inspect.iscoroutinefunction(item.function):
            task = test_wrapper(item)
            item_by_coro[task] = item
            tasks.append(task)
        else:
            item.runtest = not_coroutine_failure
            item.ihook.pytest_runtest_protocol(item=item, nextitem=None)

    async def run_tests(tasks):
        completed = []
        while tasks:
            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED,
            )
            tasks = list(pending)

            for result in done:
                item = item_by_coro[result._coro]
                item.runtest = lambda: result.result()
                item.stop = time.time()
                item.ihook.pytest_runtest_protocol(item=item, nextitem=None)

            completed.extend(done)

        return completed

    # Start our timer
    # for item in item_by_coro.values():
    #     item.start = time.time()

    # Run the tests using cooperative multitasking
    loop = asyncio.new_event_loop()
    try:
        task = run_tests(tasks)
        loop.run_until_complete(task)
    finally:
        loop.close()

    return True
