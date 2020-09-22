from aiohttp import web
from helpers import db


class Server:
    def __init__(self):
        self.app = None
        self.started = False

    def setup_server(self):
        self.app = web.Application()
        self._app['db'] = db
        self.app.on_cleanup.append(close_db)


async def close_db(app):
    app['db'].engine.dispose()
