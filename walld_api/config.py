"""module that provides config for api service"""
from os import getenv
import logging

MAJOR_VERSION = 'v1'
VERSION = '0.0.0.1'

DB_HOST = getenv('DB_HOST', 'localhost')
DB_PORT = getenv('DB_PORT', '5432')
DB_NAME = getenv('DB_NAME', 'postgres')
DB_USER = getenv('DB_USER', 'postgres')
DB_PASS = getenv('DB_PASS', '1234')
LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=LOG_LEVEL)

log = logging.getLogger('Walld api_server')

log.info(f'got this vars!\n'
         f'DB_HOST = {DB_HOST}\n'
         f'DB_PORT = {DB_PORT}\n'
         f'DB_NAME = {DB_NAME}\n'
         f'LOG_LEVEL = {LOG_LEVEL}\n')
