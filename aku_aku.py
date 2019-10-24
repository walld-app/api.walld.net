'''This code fills db that api is looking for, providing with urls and
other stuff, kindly and jently.'''
#For now (1.10.19) it can only write things like file name, category.
#sub_category, height, weight, dominated color and url
#Need to add pillow maybe? DONE

#must run by cron every day to update db with wallpapers that sits in folders

import os
import sqlite3
import psycopg2
import psycopg2.extras
import multiprocessing
from time import sleep
import argparse
import colorgram
import requests
from PIL import Image
import config

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-c', type=int, help='how many to calculate')
PARSER.add_argument('-n', type=int, help='how many to calculate without threading')
ARGS = PARSER.parse_args()

MANAGER = multiprocessing.Manager()
color_staff = MANAGER.dict()

TABLE_COLUMNS = """CREATE TABLE pics (id int, category text,
sub_category text, file_name text, width text, \
height text, ratio text, color text, url text, locked int)""" #add locked state

#checks if base exists, if not, creates one
try:
    os.makedirs(config.SEARCH_DIR)
except FileExistsError:
    pass
if config.DB == 'postgres':
    CONN = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER_NAME, 
                        password=config.DB_PASSWORD, host=config.DB_HOST,
                        port = '5159', cursor_factory=psycopg2.extras.DictCursor)
    cursor = CONN.cursor()
    cursor2 = CONN.cursor()
    SQL = '%s'
elif config.DB == 'sqlite3':
    CONN = sqlite3.connect(config.DB_FILE)
    CONN.row_factory = sqlite3.Row#stack overflow code, learn it, dumbass
    cursor = CONN.cursor()
    cursor2 = CONN.cursor() #second cursor is needed for deleting stuff
    SQL = '?'

else:
    print('db is not recognized, use sqlite3 or postgres')
    exit(1)
    
try:
    cursor.execute('SELECT * FROM pics')
except (sqlite3.OperationalError, psycopg2.ProgrammingError):
    print('hmm')
    if config.DB == 'postgres':
        CONN.rollback()
    cursor.execute(TABLE_COLUMNS)
    CONN.commit()

def list_dir(directory):
    '''returns generated list with folders'''
    subfolders = [f.name for f in os.scandir(directory) if f.is_dir()]
    return subfolders

def get_id():
    '''gets id based on existing maximun, returns -1 if didn`t find anything'''
    try:
        cursor.execute('SELECT MAX(id) FROM pics DESC LIMIT 1')
    except psycopg2.ProgrammingError:
        CONN.rollback()
        return -1
    row = cursor.fetchone()
    if row[0]:
        return row[0]
    return -1

def sync_add():
    '''recursivly walks on given folder and adds it
    to db using folder name as category'''
    idd = get_id()+1
    for category in list_dir(config.SEARCH_DIR):
        print('entering  category:' + category)

        for sub_category in list_dir(config.SEARCH_DIR + category):
            print('-'*30 + '>' + sub_category + '<' + '-'*30)

            for filename in os.listdir(config.SEARCH_DIR +
                                       category + '/'+
                                       sub_category):
                full_path = config.SEARCH_DIR + category + \
                            '/' + sub_category + '/' + filename
                sql = "SELECT file_name FROM pics WHERE file_name={}".format(SQL)
                cursor.execute(sql, (filename,))
                found_row = cursor.fetchone()
                if not found_row:
                    print(filename, 'is new here')

                    with Image.open(full_path) as img:
                        width, height = img.size
                    command = [(idd, category, sub_category, filename,
                                width, height, 'ratio_here', 'no_color',
                                config.PART_OF_URL + category + '/' + \
                                sub_category + '/' + filename, '0')]
                    cursor.executemany("INSERT INTO pics \
                                        VALUES ({0}, {0}, {0}, {0}, \
                                        {0}, {0}, {0}, {0}, {0}, {0})".format(SQL)
                                        , command)
                    idd += 1

def sync_del():
    '''This section emplements deleting non existing file.
    if file was deleted for some reason, than we need to update our db'''
    print('*'*33, 'DELETE', '*'*32)
    try:
        for row in cursor.execute('SELECT * FROM pics'):
            file_path = config.SEARCH_DIR + row['category'] + \
            '/' + row['sub_category'] + '/' + row['file_name']
        
            if not os.path.exists(file_path):
                print('deleting', file_path, 'from sql base')
                sql = "DELETE FROM pics WHERE file_name = {}".format(SQL)
                cursor2.execute(sql, (row['file_name'],))
    except TypeError:
        print('nothing to delete')
            # if we attempt to delete something on cursor
            # then whole row will vanish

def get_dom_color(img, hex_type=True):# maybe we need some rewrite to return tuple of em?
    '''gets dominant color'''
    colors = colorgram.extract(img, 1)
    print(colors)
    if hex_type : return '#%02x%02x%02x' % colors[0].rgb
    return colors[0].rgb

def calc_colors(row): 
    '''gives get_dom_color function args and writes output to dict'''
    r = requests.get(row['url'])
    file_path = config.TEMP_FOLDER + row['file_name']
    if r.status_code == 200:
        open(file_path, 'wb').write(r.content)
    else:
        print('some kind of error, need to check', row)
    color = get_dom_color(file_path)
    color_staff[str(row['id'])] = color
    os.remove(file_path)


def main():
    '''main boy'''
    procs = []
    alive = True
    ids = []
    sync_add()
    sync_del()
    CONN.commit()
    cursor.execute("SELECT * FROM pics WHERE color = 'no_color' AND locked = '0'")
    sql = "UPDATE pics SET color = {0} WHERE id = {0}".format(SQL) #add LOCKED state

    if ARGS.c:
        for _ in range(ARGS.c):
            row = cursor.fetchone()
            if row:
                cursor2.execute("UPDATE pics SET locked = '1' WHERE id = '{}'".format(row['id']))
                CONN.commit()
                ids.append(row['id'])
                thread = multiprocessing.Process(target=calc_colors,
                                             args=(row,))
                procs.append(thread)
                thread.start()
        while alive:
            get = []
            for i in procs:
                get.append(i.is_alive())
            if not any(get):
                alive = False
                if color_staff:
                    print(color_staff)
                else:
                    print('nothing to calc!')
            sleep(1)

    elif ARGS.n:
        for _ in range(ARGS.n):
            row = cursor.fetchone()
            cursor.execute("UPDATE pics SET locked = '1' WHERE id = '{}'".format(row['id']))
            CONN.commit()
            calc_colors(row)
            ids.append(row['id'])

    for i in ids:
        cursor.execute("UPDATE pics SET locked = '0' WHERE id = '{}'".format(i))
    for key in color_staff:
        cursor.execute(sql, (color_staff[key], key))

    CONN.commit()
    CONN.close()
main()
