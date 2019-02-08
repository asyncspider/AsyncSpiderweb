from os import path

from apscheduler.schedulers.tornado import TornadoScheduler

basedir = path.dirname(path.abspath(__file__))
storage_dir = path.join(basedir, 'filestorage')
project = 'Octopus'
schedulers = TornadoScheduler()
database = path.join(basedir, project+'.db')
settings = {
    "media": path.join(path.dirname(path.abspath(__file__)), 'media')
}

default_page = 50