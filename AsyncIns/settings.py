from os import path

from component.scheduler.base import TornadoScheduler

schedulers = TornadoScheduler()

basedir = path.dirname(path.abspath(__file__))
storage_dir = path.join(basedir, 'filestorage')
temp_dir = path.join(basedir, 'temp')
project = 'AsyncIns'
database = path.join(basedir, project+'.db')
secret = 'A7#s9y08n2c5In6s'
expire = 1 * 24 * 3600
default_page = 50
spider_log_path = path.join(basedir, 'logs/spiders')
settings = {
    "media": path.join(path.dirname(path.abspath(__file__)), 'media'),

}
