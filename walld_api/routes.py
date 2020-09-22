"""main launcher of api"""
from aiohttp import web

from views import health_check, get_info, get_picture
from config import MAJOR_VERSION


def setup_routes(app):
    app.router.add_get('/', health_check)
    app.router.add_get(f'/{MAJOR_VERSION}', get_info)
    app.router.add_get(f'/{MAJOR_VERSION}/walls', get_picture)
