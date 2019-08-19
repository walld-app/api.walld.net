#This code fills db that api is looking for, providing with urls and
#other stuff, kindly and jently.
#For now (12.08.19) it can only write things like file name, category.
#sub_category and url
#Need to add pillow maybe? DONE

#must run by cron every day to update db with wallpapers that sits in folders

import os, sqlite3
from PIL import Image

TABLE_COLUMNS = """CREATE TABLE pics (id text, category text,
sub_category text, file_name text, width text, \
height text, ratio text, url text)"""

#checks if base exists, if not, creates one
if os.path.exists(config.DB_FILE):
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row#stack overflow code, learn it, dumbass
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM pics')
    except sqlite3.OperationalError:
        print('hmm')
        cursor.execute(TABLE_COLUMNS)
        conn.commit()
else:
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(TABLE_COLUMNS)
    conn.commit()

def list_dir(dir):
    subfolders = [f.name for f in os.scandir(dir) if f.is_dir() ]
    return subfolders

def sync_add():
    #что если сделать из этого функцию и
    #рекурсивно ходить по папкам? типа папки абстракт и искусство будут
    #использованы названия папок в качестве темы - ГОТОВО
    for category in list_dir(config.SEARCH_DIR):
        print('entering  category:' + category)
        for sub_category in list_dir(config.SEARCH_DIR + category):
            print('-'*30 + '>' + sub_category + '<' + '-'*30)
            for filename in os.listdir(config.SEARCH_DIR +
            category + '/'+ sub_category):
                full_path = config.SEARCH_DIR + category + \
                '/' + sub_category + '/' + filename
                sql = "SELECT file_name FROM pics WHERE \
                file_name='{}'".format(filename)
                cursor.execute(sql)
                ll = cursor.fetchone()
                if not ll:
                    print(filename, 'is new here')
                    with Image.open(full_path) as img:
                        width, height = img.size
                    command = [('id_here', category, sub_category, filename,\
                    width, height, 'ratio_here', config.PART_OF_URL + \
                    category + '/' + sub_category + '/' + filename)]
                    cursor.executemany("INSERT INTO pics \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)", command)

def sync_del():
    print('*'*33, 'DELETE','*'*32)
    '''This section emplements deleting non existing file.
    if file was deleted for some reason, than we need to update our db'''
    for i in cursor.execute('SELECT * FROM pics'):
        file_path = config.SEARCH_DIR + i['category'] + \
        '/' + i['sub_category'] + '/' + i['file_name']
        if not os.path.exists(file_path):
            print('deleting', file_path, 'from sql base')
            sql = "DELETE FROM pics WHERE file_name = '{}'"\
            .format(i['file_name'])
            cursor.execute(sql)

def main():
    sync_add()
    sync_del()
    conn.commit()
    conn.close()

main()
