'''all methods of api stored here'''
from aiohttp import web
from config import VERSION
from helpers import db, get_cats_sub_cats, ApiRequest, ApiPicAnswer
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

    if 'tags' in questions:
        json['tags'] = db.named_tags

    return web.json_response(json)

def get_picture(request):
    questions = request.query
    if not questions:
        pic = choice(db.picture_objects) # nosec
    else:
        questions = ApiRequest(**questions)
        if questions.sub_category and not questions.category:
            raise web.HTTPClientError
        pics = db.get_pics(**questions.dict())

        if not pics:
            raise web.HTTPNotFound
        pic = choice(pics) # nosec

    pic = ApiPicAnswer(**pic.__dict__)

    return web.json_response(pic.dict())
