#!/usr/bin/python3
import flask
from random import choice
import sqlite3
import config
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = config.DEBUG
__version__ = '01'

def dict_factory(cursor, row): # need to make success line
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Hi</h1>
<p>This is a prototype API for sharing wallpapers.</p>'''

#@app.route('/apiv01/all', methods=['GET'])
#def api_all():
#    conn = sqlite3.connect(config.DB_FILE)
#    conn.row_factory = dict_factory
#    cur = conn.cursor()
#    all_books = cur.execute('SELECT * FROM pics;').fetchall()
#    return flask.jsonify(all_books)

#@app.route('/apiv01/random', methods=['GET'])
#def api_random():
#    conn = sqlite3.connect(config.DB_FILE)
#    conn.row_factory = dict_factory
#    cur = conn.cursor()
#    all_books = cur.execute('SELECT * FROM pics').fetchall()
#    return flask.jsonify({'success':True, 'content':choice(all_books)})

@app.route('/apiv01/', methods=['GET'])
def api_version():
    return flask.jsonify({'success':True, 'content': {'version' : __version__}})

@app.route('/apiv01/walls')
def deliver_walls():
    category = request.args.getlist('category')
    sub_category = request.args.getlist('sub_category')
    random = request.args.getlist('random')
    query = "SELECT * FROM pics WHERE"
    to_filter = []
    if random:
        conn = sqlite3.connect(config.DB_FILE)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        all_books = cur.execute('SELECT * FROM pics').fetchall()
        return flask.jsonify({'success':True, 'content':choice(all_books)})
    if category:
        for i in category:
            print('going to cycle',i)
            query += ' category=? OR'
            to_filter.append(i)
    #if sub_category:
    #    query += ' sub_category=? AND'
    #    to_filter.append(sub_category)
    if not (category or random):
        return page_not_found(404)
    query = query[:-3] + ';'
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    result = cur.execute(query, to_filter).fetchall()
    return flask.jsonify(choice(result))

@app.errorhandler(404)
def page_not_found(e):
    return flask.jsonify({'error':'404', 'success':False}), 404

app.run()
