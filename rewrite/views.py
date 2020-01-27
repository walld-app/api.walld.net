'''all methods of api stored here'''
from aiohttp import web

def healthcheck(req):
    '''simplehealthcheck'''
    del req
    return web.Response()
