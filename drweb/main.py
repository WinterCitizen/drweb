import asyncio

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

import settings
from handlers import routes


def cancel_all(coros):
    for coro in coros:
        coro.cancel()


def init_app(loop):
    app = web.Application()
    app.add_routes(routes)

    app['db'] = AsyncIOMotorClient(
        settings.MONGO_HOST, settings.MONGO_PORT, io_loop=loop)

    return app


def main(port):
    loop = asyncio.get_event_loop()
    app = init_app(loop)

    try:
        web.run_app(app, port=port)
    except KeyboardInterrupt:
        pending = asyncio.all_tasks()

        cancel_all(pending)


if __name__ == '__main__':
    main(8000)
