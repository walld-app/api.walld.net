'''This code fills db that api is looking for, providing with urls and
other stuff, kindly and jently.'''
#For now (1.10.19) it can only write things like file name, category.
#sub_category, height, weight, dominated color and url
#Need to add pillow maybe? DONE

#must run by cron every day to update db with wallpapers that sits in folders

import os
import sqlite3
from PIL import Image
import colorgram
import config

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

def get_dom_color(img, hex_type=True):
    '''gets dominant ONE color'''
    colors = colorgram.extract(img, 1)
    if hex_type:
        print(colors[0].rgb)
        return '#%02x%02x%02x' % colors[0].rgb
    return colors[0].rgb

def sync_add():
    '''recursivly walks on given folder and adds it
    to db using folder name as category'''
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

                    command = [('1', category, sub_category, filename,
                                width, height, 'ratio_here', 'color_here',
                                config.PART_OF_URL + category + '/' + \
                                sub_category + '/' + filename)]
                    cursor.executemany("INSERT INTO pics \
                                        VALUES (?, ?, ?, ?, \
                                        ?, ?, ?, ?, ?)", command)

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
            # if we attempt to delete something on cursor then whole row will vanish

def main():
    '''main boy'''
    sync_add()
    sync_del()
    CONN.commit()
    CONN.close()

main()
