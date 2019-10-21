import config

class Sql_boy():
    def __init__(self, db_type = None):
        self.db_type = db_type
        if self.db_type == 'postgres':
            import psycopg2
            import psycopg2.extras
            self.CONN = psycopg2.connect(
                dbname=config.DB_NAME, user=config.DB_USER_NAME, 
                password=config.DB_PASSWORD, host=config.DB_HOST,
                port = '5159', cursor_factory=psycopg2.extras.DictCursor
            )
            self.cursor = self.CONN.cursor()
            self.cursor2 = self.CONN.cursor()
            self.SQL = '%s'

        elif self.db_type == 'sqlite3':
            import sqlite3
            self.CONN = sqlite3.connect(config.DB_FILE, check_same_thread=False)
            self.CONN.row_factory = sqlite3.Row#stack overflow code, learn it, dumbass
            self.cursor = self.CONN.cursor()
            self.cursor2 = self.CONN.cursor()
            self.SQL = '?'

        elif not self.db_type:
            print('you didn`t specify db name in config!')
            exit(1)
    
    def execute(self, line, args = (), fetch='all'):
        line += ';'
        if self.db_type == 'postgres':
            self.cursor.execute(line)
        elif self.db_type == 'sqlite3':
            result = self.cursor.execute(line)

        if fetch == 'all':
            if self.db_type == 'postgres':
                return self.cursor.fetchall()
            return result.fetchall()
        elif fetch == 'one':
            if self.db_type == 'postgres':
                return self.cursor.fetchone()
            return self.cursor.fetchone()
         
