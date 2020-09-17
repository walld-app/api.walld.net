"""module that provides config for api service"""
from os import getenv
from walld_db.helpers import logger_factory
from pathlib import Path

_PROJECT_DIR = Path(__file__).parents[1]
ENV_PATH = _PROJECT_DIR / '.env'

try:
    from dotenv import load_dotenv
    if ENV_PATH.exists():
        load_dotenv(dotenv_path=str(ENV_PATH), override=False)
except ImportError:
    pass

MAJOR_VERSION = 'v1'
VERSION = '0.0.0.1'

DB_HOST = getenv('DB_HOST', 'localhost')
DB_PORT = getenv('DB_PORT', '5432')
DB_NAME = getenv('DB_NAME', 'postgres')
DB_USER = getenv('DB_USER', 'postgres')
DB_PASS = getenv('DB_PASS', '1234')
LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')

log = logger_factory('Walld api_server', level=LOG_LEVEL)

if ENV_PATH.exists():
    log.info(f'Loaded vars from .env file {str(ENV_PATH)}')

log.info(f'got this vars!\n'
         f'DB_HOST = {DB_HOST}\n'
         f'DB_PORT = {DB_PORT}\n'
         f'DB_NAME = {DB_NAME}\n'
         f'LOG_LEVEL = {LOG_LEVEL}\n')
