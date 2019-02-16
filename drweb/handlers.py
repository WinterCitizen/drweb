import asyncio

from aiohttp.web import RouteTableDef, json_response
from bson import ObjectId
from funcy import walk_values

import store
import tasks

routes = RouteTableDef()


@routes.get('/')
async def create_task(request):
    app = request.app
    task_id = await store.create_task(app['db'])

    asyncio.create_task(tasks.run_task(app['db'], task_id))

    return json_response(dict(task_id=str(task_id)))


def _valid_task_id(task_id):
    return ObjectId.is_valid(task_id)


@routes.get(r'/{task_id:\w+}/')
async def get_task(request):
    app = request.app

    raw_task_id = request.match_info['task_id']
    if not _valid_task_id(raw_task_id):
        return json_response({'errors': ['Parameter task_id is not valid']})

    task_id = ObjectId(raw_task_id)

    task = await store.get_task(app['db'], task_id)
    if task is None:
        return json_response(
            {'errors': ['Task with provided id is not found']})

    return json_response(walk_values(str, task))
