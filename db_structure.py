'''this module describes how db will go'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

BASE = declarative_base()


class BaseTable(BASE):
    '''abstract model for all tables.'''
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    rating = Column(Integer)

class WalldPics(BaseTable):
    '''represents wall from db point of view'''
    __tablename__ = 'walls'
    width = Column(Integer)
    height = Column(Integer)
    ratio = Column(String)
    color = Column(String)
    category = Column(String)
    sub_category = Column(String)
    file_name = Column(String)
    locked = Column(Boolean)


class WalldUser(BaseTable):
    '''represents user from db point of view'''
    __tablename__ = 'users'
    uploads = Column(Integer)

