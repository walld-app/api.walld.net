import config


#ПИЗДЕЦ НУЖНО ПИСАТЬ ЕБАНЫЙ ДИКФАКТОРИ

class Sql_boy():
    def __init__(self, db_type = None):
        self.db_type = db_type
        if self.db_type == 'postgres':
            import psycopg2
            import psycopg2.extras
            self.CONN = psycopg2.connect(
                dbname=config.DB_NAME, user=config.DB_USER_NAME, 
                password=config.DB_PASSWORD, host=config.DB_HOST,
                port = '5159', cursor_factory=psycopg2.extras.RealDictCursor
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
    

    def execute(self, line, args = None, fetch='all'):
        line += ';'
        if self.db_type == 'postgres': #kind of spaghetti code
            dd = {}
            self.cursor.execute(line, args)
        elif self.db_type == 'sqlite3':
            result = self.cursor.execute(line)

        if fetch == 'all':
            if self.db_type == 'postgres':
                list_of_dicts = []
                fetchall = self.cursor.fetchall()
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
                for i in ll:
                    dd[i] = ll[i]
                return dd
            return result.fetchone()

    def gen_line(self, line):
        return line.format(self.SQL)

    def close_connection(self):
        self.CONN.close()
