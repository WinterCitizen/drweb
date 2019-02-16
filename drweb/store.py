from datetime import datetime, timezone
from enum import Enum

from funcy import get_in

import settings


class Status(Enum):
    """
    Assuming `time.sleep()` can't fail, so no ERROR status.
    """

    IN_QUEUE = 'In Queue'
    RUN = 'Run'
    COMPLETE = 'Complete'


TASKS = 'tasks'


def get_collection(db, collection):
    return get_in(db, [settings.MONGO_DB_NAME, collection])


def _now():
    return datetime.now(timezone.utc)


async def create_task(db):
    tasks = get_collection(db, TASKS)
    result = await tasks.insert_one(
        dict(
            status=Status.IN_QUEUE.value,
            create_time=_now(),
            start_time='',
            execution_time=''))

    return result.inserted_id


async def set_task_running(db, task_id):
    tasks = get_collection(db, TASKS)
    result = await tasks.update_one(
        {'_id': task_id},
        {'$set': {
            'status': Status.RUN.value,
            'start_time': _now()}})

    return result.matched_count


async def set_task_complete(db, task_id, execution_time):
    tasks = get_collection(db, TASKS)
    result = await tasks.update_one(
        {'_id': task_id},
        {'$set': {
            'status': Status.COMPLETE.value,
            'execution_time': execution_time}})

    return result.matched_count


async def get_task(db, task_id):
    tasks = get_collection(db, TASKS)
    return await tasks.find_one({'_id': task_id})
