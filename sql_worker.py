''' sql worker module that helps with quering'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_structure import BASE
from helpers import get_connection_dsn

ENGINE = create_engine(get_connection_dsn())
BASE.metadata.create_all(ENGINE) # REDO TO ALEMBIC 
SESSION = sessionmaker(bind=ENGINE)

def get_distinct(target):
    '''gets distinct values by CLASS.COLUMN'''
    try:
        session = SESSION()
        distincts = [i[0] for i in session.query(target).distinct()] #КОСТЫЛЬ ПЕРЕДЕЛАТЬ
        return distincts
    except :# докинуть ошибку
        print('error')