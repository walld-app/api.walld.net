'''main launcher of api'''
from aiohttp import web

from views import healthcheck


APP = web.Application()
APP.router.add_get('/', healthcheck)


web.run_app(APP)
S