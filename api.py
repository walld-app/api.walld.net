'''main launcher of api'''
from aiohttp import web

from views import healthcheck, get_info
from config import VERSION 

APP = web.Application()
APP.router.add_get('/', healthcheck)
APP.router.add_get(f'/api/{VERSION}', get_info)

web.run_app(APP)