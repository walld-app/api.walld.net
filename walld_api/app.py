from aiohttp import web
from helpers import db
from routes import setup_routes


class Server:
    def __init__(self):
        self.app = None
        self.started = False

    def setup_server(self):

        assert not self.started, "Server already started"
        self.started = True

        self.app = web.Application()
        self.app['db'] = db
        self.app.on_cleanup.append(close_db)

        setup_routes(self.app)

    def run(self, http_port=None):
        """Run aiohttp server."""
        if not self.started:
            self.setup_server()

        web.run_app(self.app)





async def close_db(app):
    app['db'].engine.dispose()
