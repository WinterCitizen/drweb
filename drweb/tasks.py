import asyncio
import random
import time
from concurrent.futures.thread import ThreadPoolExecutor

import settings
from store import set_task_complete, set_task_running

semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_TASKS)


def task():
    time.sleep(random.randint(0, 10))


async def run_task(db, task_id):
    loop = asyncio.get_event_loop()

    async with semaphore:
        await set_task_running(db, task_id)

        started = time.monotonic()
        await loop.run_in_executor(ThreadPoolExecutor(None), task)

        await set_task_complete(
            db, task_id, execution_time=time.monotonic() - started)
