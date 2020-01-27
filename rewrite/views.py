'''all methods of api stored here'''
from aiohttp import web
from config import VERSION
from sql_worker import get_distinct
from db_structure import WalldPics

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
        list_ = get_distinct(WalldPics.category)
        json['categories'] = list_

    return web.json_response(json)
    