from aiohttp import web
from routes import APP

if __name__ == '__main__':
    web.run_app(APP)