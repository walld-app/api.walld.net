'''postgresql and sqlite3 lib for DRY code'''
import sqlite3
import sys
import psycopg2
import psycopg2.extras
import config

class SqlBoy():
    '''class represents connection for postgre and(in future) sqlite3'''
    def __init__(self, db_type=None):
        self.db_type = db_type
        self.table_columns = """CREATE TABLE pics (id int, category text, \
                            sub_category text, file_name text, width text, \
                            height text, ratio text, color text, url text, locked int)"""
        if self.db_type == 'postgres':
            self.conn = psycopg2.connect(
                dbname=config.DB_NAME, user=config.DB_USER_NAME,
                password=config.DB_PASSWORD, host=config.DB_HOST,
                port=config.DB_PORT, cursor_factory=psycopg2.extras.RealDictCursor
            )
            self.cursor = self.conn.cursor()
            self.cursor2 = self.conn.cursor()
            self.sql = '%s'

        elif self.db_type == 'sqlite3':
            self.conn = sqlite3.connect(config.DB_FILE, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row#stack overflow code, learn it, dumbass
            self.cursor = self.conn.cursor()
            self.cursor2 = self.conn.cursor()
            self.sql = '?'

        elif not self.db_type:
            print('you didn`t specify db name in config!')
            sys.exit(1)

        try:
            self.cursor.execute('SELECT * FROM pics')
        except (sqlite3.OperationalError, psycopg2.ProgrammingError):
            if self.db_type == 'postgres':
                self.conn.rollback()
            self.cursor.execute(self.table_columns)
            self.conn.commit()

    def execute(self, line, args=None, fetch='all'):
        '''executes line with or without args'''
        line += ';'
        row_dicts = {}
        try:
            self.cursor.execute(line, args)
        except psycopg2.ProgrammingError:
            self.conn.rollback()
            return row_dicts
        result = self.cursor.execute(line, args)
        if fetch == 'all':
            if self.db_type == 'postgres':
                list_of_dicts = []
                try:
                    fetchall = self.cursor.fetchall()
                except psycopg2.ProgrammingError:
                    return row_dicts
                for row in fetchall:#NEED NEW FUNCTION AND
                    for content in row:#POSSIBLY CONTRIBUTE THIS
                        row_dicts[content] = row[content]#TO PSYCOPG2, AWFUL
                    list_of_dicts.append(row_dicts)
                    row_dicts = {}
                return list_of_dicts

        elif fetch == 'one':
            if self.db_type == 'postgres':
                list_of_lines = self.cursor.fetchone()
                if not list_of_lines:
                    return row_dicts
                for i in list_of_lines:
                    row_dicts[i] = list_of_lines[i]
                return row_dicts
            return result.fetchone()

    def gen_line(self, line):
        '''gens line based on sql format'''
        return line.format(self.sql)

    def commit(self):
        '''commits changes'''
        self.conn.commit()

    def close_connection(self):
        '''closes connection'''
        self.conn.close()
