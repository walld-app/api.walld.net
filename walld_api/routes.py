'''main launcher of api'''
from aiohttp import web

from views import health_check, get_info, get_picture
from config import MAJOR_VERSION

APP = web.Application()
APP.router.add_get('/', health_check)
APP.router.add_get(f'/{MAJOR_VERSION}', get_info)
APP.router.add_get(f'/{MAJOR_VERSION}/walls', get_picture)
