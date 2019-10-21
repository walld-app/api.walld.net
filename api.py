#!/usr/bin/python3
#НЕОБХОДИМО НАПИСАТЬ КЛАСС ДЛЯ БАЗЫ ДАННЫХ ЭТО ЖЕСТЬ
import flask
from random import choice
import sqlite3
import sql_worker
import config
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = config.DEBUG
__version__ = '02'
sql_boy = sql_worker.Sql_boy(db_type = config.DB)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Hi</h1>
<p>This is a prototype API for sharing wallpapers.</p>'''

@app.route('/apiv01/', methods=['GET'])
def api_version():
    param = request.args.get('param')# listens ?param=

    if param == 'categories':
        query = "SELECT DISTINCT category FROM pics"
        result = sql_boy.execute(query, fetch = 'all')
        print(result, 'this is result')

        for category in result:
            print(category, 'this is category') # НИЧЕ НЕ ПОНЯТНО АЛЛОУ
            query = "SELECT DISTINCT sub_category\
             FROM pics WHERE category ='{}'".format(category['category'])
            ll = sql_boy.execute(query, fetch = 'all')
            print(ll[0], 'this is ll')
            category['subs'] = [] # refactor
            for k in ll:

                i['subs'].append(k['sub_category'])
            print('this is i', i)
        return flask.jsonify({'success':True, 'content': result })

    elif param == 'version':
        return flask.jsonify({'success':True, 'content': {'version' : __version__}})

    else:
        return page_not_found(404)

@app.route('/apiv01/walls')
def deliver_walls():
    category = request.args.getlist('category')
    sub_category = request.args.getlist('sub_category')
    random = request.args.getlist('random')
    query = "SELECT * FROM pics WHERE"
    to_filter = []
    if random:
        all_walls = sql_boy.execute('SELECT * FROM pics', fetch = 'all')
        return flask.jsonify({'success':True, 'content':choice(all_walls)})
    if category:
        for i in category:
            print('going to cycle',i)
            query += ' category={}'. format(sql_boy.SQL)
            to_filter.append(i)
    if sub_category:
        query += ' AND'
        for i in sub_category:
            print('some subcategories', i)
            query += ' sub_category={}'.format(sql_boy.SQL)
            to_filter.append(i)
    if not (category or random):
        return page_not_found(404)
    query += ';'
    print(query)
    print(to_filter)
    result = sql_boy.execute(query, args=to_filter, fetch='all')
    if result:
        return flask.jsonify({'success':True, 'content':choice(result)})
    else:
        return page_not_found(404)

@app.errorhandler(404)
def page_not_found(e):
    return flask.jsonify({'error':'404', 'success':False}), 404

app.run()
