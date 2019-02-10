from os import path

from component.scheduler.base import TornadoScheduler
# from apscheduler.schedulers.tornado import TornadoScheduler

basedir = path.dirname(path.abspath(__file__))
storage_dir = path.join(basedir, 'filestorage')
project = 'Octopus'
schedulers = TornadoScheduler()
database = path.join(basedir, project+'.db')
settings = {
    "media": path.join(path.dirname(path.abspath(__file__)), 'media'),

}
secret = 'A7#s9y08n2c5In6s'
expire = 1 * 24 * 3600
default_page = 50

model = ('Increase', 'RunRecord', 'TaskQueue', 'JobStore', 'User',
         'SuperUser', '')