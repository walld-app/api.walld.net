'''main launcher of api'''
from aiohttp import web

from views import healthcheck, get_info, get_random_picture
from config import VERSION 

APP = web.Application()
APP.router.add_get('/', healthcheck)
APP.router.add_get(f'/{VERSION}', get_info)
APP.router.add_get(f'/{VERSION}/walls', get_random_picture)

web.run_app(APP)