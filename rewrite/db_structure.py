'''this module describes how db will go'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

BASE = declarative_base()


class walld_pics(BASE):
    '''represents wall from db point of view'''
    walld_id = Column(Integer, primary_key=True)
    width = Column(Integer)
    height = Column(Integer)
    color = Column(String)
    category = Column(String)
    sub_category = Column(String)
    file_name = Column(String)
    ratio = Column(String)
    locked = Column(Boolean)


class walld_user(BASE):
    '''represents user from db point of view'''
    user_id = Column(Integer, primary_key=True)