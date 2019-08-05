import flask
from random import choice
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row): # need to make success line
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Hi</h1>
<p>This is a prototype API for sharing wallpapers.</p>'''

@app.route('/apiv01/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('pics.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()
    return jsonify(all_books)

@app.route('/apiv01/random', methods=['GET'])
def api_random():
    conn = sqlite3.connect('pics.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM pics;').fetchall()
    return jsonify(choice(all_books))

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error':'404', 'success':'false'}), 404

app.run()
