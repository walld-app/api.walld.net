#must run by cron every day to update db with wallpapers that sits in folders
#and delete non-existing(404) ones
#also rms old files
import os, sqlite3
SEARCH_DIR = '/mnt/ntfs-drive/walld_pics/'
DB_FILE = SEARCH_DIR + 'pics.db'
PART_OF_URL = 'http://walld.net/pics/'

TABLE_COLUMNS = """CREATE TABLE pics (id text, category text, sub_cat text, file_name text, resolution text, ratio text, url text)"""
#checks if base exists, if not, creates one
if os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = lambda cursor, row: row[0]
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM pics')
    except sqlite3.OperationalError:
        cursor.execute(TABLE_COLUMNS)
        conn.commit()
else:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = lambda cursor, row: row[0]
    cursor = conn.cursor()
    cursor.execute(TABLE_COLUMNS)
    conn.commit()

#this section makes db that api is looking for, providing with urls and other stuff, kindly and jently
#for now (07.08.19) it can only write things like file name and url, pillow maybe?

for filename in os.listdir(SEARCH_DIR): # что если сделать из этого функцию и рекурсивно ходить по папкам? типа папки абстракт и искусство будут использованы названия папок в качестве темы
    sql = "SELECT file_name FROM pics WHERE file_name='"+filename+"'"
    cursor.execute(sql)
    ll = cursor.fetchone() # or use fetchone()
    if ll == filename:
        pass
    else:
        print(filename, 'is new here')
        command = [('nope', 'abstract', 'nope', filename,\
         'nope', 'nope', PART_OF_URL + filename)]
        cursor.executemany("INSERT INTO pics VALUES (?, ?, ?, ?, ?, ?, ?)", command)
conn.commit()
#This section emplements that if file was deleted for some reason, than we need to update our db

list = cursor.execute("SELECT file_name FROM pics").fetchall()
for filename in list:
    if os.path.exists(SEARCH_DIR + filename):
        pass
    else:
        print('deleting', filename)
        sql = "DELETE FROM pics WHERE file_name = ?"
        cursor.execute(sql, [(filename)])
conn.commit()

#Here comes part where it double checks thaat everything is accesseble,
#i dont know,  maybe we dont need this part at all bc we have file check and aku_aku should trust web engine

#list = cursor.execute("SELECT url FROM pics").cursor.fetchall()
#for url in list:
