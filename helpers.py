'''helpers module provides some functions'''

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

def get_connection_dsn():
    return f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

def ll(sda0) -> int:
    pass