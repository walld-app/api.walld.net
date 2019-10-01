#This code fills db that api is looking for, providing with urls and
#other stuff, kindly and jently.
#For now (12.08.19) it can only write things like file name, category.
#sub_category and url
#Need to add pillow maybe? DONE

#must run by cron every day to update db with wallpapers that sits in folders

import os, sqlite3, config
from PIL import Image
import colorgram

TABLE_COLUMNS = """CREATE TABLE pics (id int, category text,
sub_category text, file_name text, width text, \
height text, ratio text, color text, url text)"""

#checks if base exists, if not, creates one
if os.path.exists(config.DB_FILE):
    os.makedirs(config.SEARCH_DIR)
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row#stack overflow code, learn it, dumbass
    cursor = conn.cursor()
    cursor2 = conn.cursor() #second cursor is needed for deleting stuff
    try:
        cursor.execute('SELECT * FROM pics')
    except sqlite3.OperationalError:
        print('hmm')
        cursor.execute(TABLE_COLUMNS)
        conn.commit()
else:
    os.makedirs(config.SEARCH_DIR)
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    cursor.execute(TABLE_COLUMNS)
    conn.commit()

def list_dir(directory):
    subfolders = [f.name for f in os.scandir(directory) if f.is_dir() ]
    return subfolders

def get_dom_color(img, hex=True):
    '''gets dominant ONE color'''
    colors = colorgram.extract(img, 1)
    if hex:
        print(colors[0].rgb)
        return '#%02x%02x%02x' % colors[0].rgb
    else:
        return colors[0].rgb

def sync_add():
    '''recursivly walks on given folder and adds it
    to db using folder name as category'''
    for category in list_dir(config.SEARCH_DIR):
        print('entering  category:' + category)
        for sub_category in list_dir(config.SEARCH_DIR + category):
            print('-'*30 + '>' + sub_category + '<' + '-'*30)
            for filename in os.listdir(config.SEARCH_DIR +
            category + '/'+ sub_category):
                full_path = config.SEARCH_DIR + category + \
                '/' + sub_category + '/' + filename
                sql = "SELECT {} FROM {} WHERE \
                {}='{}'".format('file_name','pics', 'file_name', filename)
                cursor.execute(sql)
                ll = cursor.fetchone()
                if not ll:
                    print(filename, 'is new here')
                    with Image.open(full_path) as img:
                        width, height = img.size
                    command = [('1', category, sub_category, filename,\
                    width, height, 'ratio_here', 'color_here', \
                    config.PART_OF_URL + \
                    category + '/' + sub_category + '/' + filename)]
                    cursor.executemany("INSERT INTO pics \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", command)

def sync_del():
    '''This section emplements deleting non existing file.
    if file was deleted for some reason, than we need to update our db'''
    print('*'*33, 'DELETE','*'*32)

    for row in cursor.execute('SELECT * FROM pics'): 
        file_path = config.SEARCH_DIR + row['category'] + \
        '/' + row['sub_category'] + '/' + row['file_name']
        if not os.path.exists(file_path):
            print('deleting', file_path, 'from sql base')
            sql = "DELETE FROM pics WHERE file_name = ?"
            cursor2.execute(sql, (row['file_name'],))
            # if we attempt to delete something on cursor then whole row will vanish

def main():
    sync_add()
    sync_del()
    conn.commit()
    conn.close()

main()
