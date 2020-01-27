#!/usr/bin/python3
'''api implementation in python'''
from random import choice
import flask
from flask import request
import sql_worker
import config

app = flask.Flask(__name__)
app.config["DEBUG"] = config.DEBUG
__version__ = '02'
sql_boy = sql_worker.SqlBoy(db_type=config.DB)

@app.route('/', methods=['GET'])
def home():
    '''returns "home" page'''
    return '''<h1>Hi</h1>
<p>This is a prototype API for sharing wallpapers.</p>'''

@app.route('/apiv01/', methods=['GET'])
def api_version():
    '''some info about api and other stored here'''
    param = request.args.get('param')# listens ?param=
    if param == 'categories':
        query = "SELECT DISTINCT category FROM pics"
        result = sql_boy.execute(query, fetch='all')
        for category in result:
            query = sql_boy.gen_line("SELECT DISTINCT sub_category \
                                       FROM pics WHERE category = {0}")
            sub_categories = sql_boy.execute(query, args=(category['category'], ), fetch='all')
            category['subs'] = [] # refactor
            for sub_category in sub_categories:
                category['subs'].append(sub_category['sub_category'])
        return flask.jsonify({'success':True, 'content': result})

    if param == 'version':
        return flask.jsonify({'success':True, 'content': {'version' : __version__}})
    return page_not_found(404)

@app.route('/apiv01/walls')
def deliver_walls():
    '''main route for accessing walls'''
    category = request.args.getlist('category')
    sub_category = request.args.getlist('sub_category')
    random = request.args.getlist('random')
    query = "SELECT * FROM pics WHERE"
    to_filter = []
    if random:
        all_walls = sql_boy.execute('SELECT * FROM pics', fetch='all')
        return flask.jsonify({'success':True, 'content':choice(all_walls)})
    if category:
        for i in category:
            print('going to cycle', i)
            query += ' category={0}'
            to_filter.append(i)
    if sub_category:
        query += ' AND'
        for i in sub_category:
            print('some subcategories', i)
            query += ' sub_category={0}'
            to_filter.append(i)
    if not (category or random):
        return page_not_found(404)
    query = sql_boy.gen_line(query)
    print(query, '< query')
    result = sql_boy.execute(query, args=to_filter, fetch='all')
    if result:
        return flask.jsonify({'success':True, 'content':choice(result)}) #nosec
    return page_not_found(404)

@app.errorhandler(404)
def page_not_found(error_code):
    '''404 route'''
    return flask.jsonify({'error':'404', 'success':False}), 404

app.run()
sql_boy.close_connection()
