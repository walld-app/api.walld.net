'''all methods of api stored here'''
from aiohttp import web
from config import VERSION
from helpers import db, get_cats_sub_cats
from random import choice

def healthcheck(request):
    '''simplehealthcheck'''
    del request
    return web.Response()

def get_info(request):
    '''answers with information about api'''
    questions = request.query
    json = {'success':'true'}

    if 'version' in questions:
        json['version'] = VERSION

    if 'categories' in questions:
        json['categories'] = get_cats_sub_cats()

    return web.json_response(json)

def get_random_picture(request):
    questions = request.query
    if 'random' in questions:
        pic = choice(db.picture_objects) # nosec
        pic = dict(pic.__dict__)
        del pic['_sa_instance_state']
        del pic['path']
        return web.json_response(pic)
