import config
import psycopg2
import psycopg2.extras
import sqlite3

#ПИЗДЕЦ НУЖНО ПИСАТЬ ЕБАНЫЙ ДИКФАКТОРИ

class Sql_boy():
    def __init__(self, db_type = None):
        self.db_type = db_type
        self.TABLE_COLUMNS = """CREATE TABLE pics (id int, category text, \
                            sub_category text, file_name text, width text, \
                            height text, ratio text, color text, url text, locked int)"""   
        if self.db_type == 'postgres':
            self.CONN = psycopg2.connect(
                dbname=config.DB_NAME, user=config.DB_USER_NAME, 
                password=config.DB_PASSWORD, host=config.DB_HOST,
                port = config.DB_PORT, cursor_factory=psycopg2.extras.RealDictCursor
            )
            self.cursor = self.CONN.cursor()
            self.cursor2 = self.CONN.cursor()
            self.SQL = '%s'

        elif self.db_type == 'sqlite3':
            self.CONN = sqlite3.connect(config.DB_FILE, check_same_thread=False)
            self.CONN.row_factory = sqlite3.Row#stack overflow code, learn it, dumbass
            self.cursor = self.CONN.cursor()
            self.cursor2 = self.CONN.cursor()
            self.SQL = '?'

        elif not self.db_type:
            print('you didn`t specify db name in config!')
            exit(1)

        try:
            self.cursor.execute('SELECT * FROM pics')
        except (sqlite3.OperationalError, psycopg2.ProgrammingError):
            if self.db_type == 'postgres':
                self.CONN.rollback()
            self.cursor.execute(self.TABLE_COLUMNS)
            self.CONN.commit()

    def execute(self, line, args = None, fetch='all'):
        line += ';'
        if self.db_type == 'postgres': #kind of spaghetti code
            dd = {}
            try:
                self.cursor.execute(line, args)
            except psycopg2.ProgrammingError:
                self.CONN.rollback()
                return False
        elif self.db_type == 'sqlite3':
            result = self.cursor.execute(line)

        if fetch == 'all':
            if self.db_type == 'postgres':
                list_of_dicts = []
                try:
                    fetchall = self.cursor.fetchall()
                except psycopg2.ProgrammingError:
                    return {}
                for row in fetchall:                #NEED NEW FUNCTION AND
                    for content in row:             #POSSIBLY CONTRIBUTE THIS 
                        dd[content] = row[content]  #TO PSYCOPG2, AWFUL
                    list_of_dicts.append(dd)
                    dd = {}
                return list_of_dicts
            return result.fetchall()

        elif fetch == 'one':
            if self.db_type == 'postgres':
                ll = self.cursor.fetchone()
                if not ll:
                    return dd
                for i in ll:
                    dd[i] = ll[i]
                return dd
            return result.fetchone()

    def gen_line(self, line):
        return line.format(self.SQL)

    def commit(self):
        self.CONN.commit()

    def close_connection(self):
        self.CONN.close()
