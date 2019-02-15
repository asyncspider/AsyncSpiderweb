from os import path

from component.bases import TornadoScheduler


schedulers = TornadoScheduler()

# Json web token expire value
EXPIRE = 1 * 24 * 3600

# Default page number
DEFAULT_PAGE = 50

# Offset threshold
DEFAULT_OFFSET = 9999

# Project base dir
BASEDIR = path.dirname(path.abspath(__file__))

# Json web token secret key
SECRET = 'A1s3y5n7c9S0p2i4d6e8r2w0e5b'

EGG_DIR = path.join(BASEDIR, 'eggs')

TEMP_DIR = path.join(BASEDIR, 'temp')

SPIDER_LOG_DIR = path.join(BASEDIR, 'logs/spiders')

