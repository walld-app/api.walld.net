'''This code fills db that api is looking for, providing with urls and
other stuff, kindly and jently.'''
#For now (1.10.19) it can only write things like file name, category.
#sub_category, height, weight, dominated color and url
#Need to add pillow maybe? DONE

#must run by cron every day to update db with wallpapers that sits in folders

import os
import sqlite3
import multiprocessing
from time import sleep
import argparse
import colorgram
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
height text, ratio text, color text, url text)"""

#checks if base exists, if not, creates one
try:
    os.makedirs(config.SEARCH_DIR)
except FileExistsError:
    pass

CONN = sqlite3.connect(config.DB_FILE)
CONN.row_factory = sqlite3.Row#stack overflow code, learn it, dumbass
cursor = CONN.cursor()
cursor2 = CONN.cursor() #second cursor is needed for deleting stuff

try:
    cursor.execute('SELECT * FROM pics')
except sqlite3.OperationalError:
    print('hmm')
    cursor.execute(TABLE_COLUMNS)
    CONN.commit()

def list_dir(directory):
    '''returns generated list with folders'''
    subfolders = [f.name for f in os.scandir(directory) if f.is_dir()]
    return subfolders

def get_id():
    '''gets id based on existing maximun, returns -1 if didn`t find anything'''
    cursor.execute('SELECT MAX(id) FROM pics DESC LIMIT 1')
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
                sql = "SELECT file_name FROM pics WHERE file_name=?"
                cursor.execute(sql, (filename,))
                found_row = cursor.fetchone()
                if not found_row:
                    print(filename, 'is new here')

                    with Image.open(full_path) as img:
                        width, height = img.size
                    command = [(idd, category, sub_category, filename,
                                width, height, 'ratio_here', 'no_color',
                                config.PART_OF_URL + category + '/' + \
                                sub_category + '/' + filename)]
                    cursor.executemany("INSERT INTO pics \
                                        VALUES (?, ?, ?, ?, \
                                        ?, ?, ?, ?, ?)", command)
                    idd += 1

def sync_del():
    '''This section emplements deleting non existing file.
    if file was deleted for some reason, than we need to update our db'''
    print('*'*33, 'DELETE', '*'*32)

    for row in cursor.execute('SELECT * FROM pics'):
        file_path = config.SEARCH_DIR + row['category'] + \
        '/' + row['sub_category'] + '/' + row['file_name']
        
        if not os.path.exists(file_path):
            print('deleting', file_path, 'from sql base')
            sql = "DELETE FROM pics WHERE file_name = ?"
            cursor2.execute(sql, (row['file_name'],))
            # if we attempt to delete something on cursor
            # then whole row will vanish

def get_dom_color(img, hex_type=True):
    '''gets dominant ONE color'''
    colors = colorgram.extract(img, 1)
    if hex_type:
        return '#%02x%02x%02x' % colors[0].rgb
    return colors[0].rgb

def calc_colors(row):
    '''gives get_dom_color function args and writes output to dict'''
    if not row:
        return False
    file_path = config.SEARCH_DIR + row['category'] + \
    '/' + row['sub_category'] + '/' + row['file_name']
    color = get_dom_color(file_path)
    color_staff[str(row['id'])] = color
    

def main():
    '''main boy'''
    sync_add()
    sync_del()
    CONN.commit()
    cursor.execute('SELECT * FROM pics WHERE color = "no_color"')
    sql = 'UPDATE pics SET color = ? WHERE color = "no_color" AND id = ?'

    if ARGS.c:
        procs = []
        alive = True
        for _ in range(ARGS.c):
            thread = multiprocessing.Process(target=calc_colors,
                                             args=(cursor.fetchone(),))
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
            calc_colors(cursor.fetchone())

    for key in color_staff:
        cursor.execute(sql, (color_staff[key], key))

    CONN.commit()
    CONN.close()
main()
