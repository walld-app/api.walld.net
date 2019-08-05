#must run by cron every hour to update db with wallpapers that sits in folders
#also rms old files 
import os, sqlite3
SEARCH_DIR = '/mnt/ntfs-drive/walld_pics'
DB_FILE = SEARCH_DIR + '/pics.db'
PART_OF_URL = 'http://walld.net/pics/'

if os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE) # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
else:
    conn = sqlite3.connect(DB_FILE) # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE pics
                  (id text, category text, sub_cat text, file_name text,
                   resolution text, ratio text, url text)
               """)
    conn.commit()

for filename in os.listdir(SEARCH_DIR):
    print(filename)
    sql = "SELECT * FROM pics WHERE file_name=?"
    cursor.execute(sql, [(filename)])
    ll = cursor.fetchone() # or use fetchone()
    if ll == filename:
        pass
    else:
        command = [('nope', 'abstract', 'nope', filename,\
         'nope', 'nope', PART_OF_URL + filename)]
        cursor.executemany("INSERT INTO pics VALUES (?, ?, ?, ?, ?, ?, ?)", command)
conn.commit()
