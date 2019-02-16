import logging
import ast
from os import path

from tornado import ioloop
from tortoise import Tortoise
from tornado.web import Application
from tornado.options import options, define

from urls import router
from settings import schedulers, TORNADO_LOG
from model import Schedulers
from component.executor.distribute import execute_task


define('port', default=8205, help='run on the given port', type=int)
define('debug', default=True, help='set tornado debug mode', type=bool)
options.log_file_prefix = TORNADO_LOG  # logs path
options.log_rotate_mode = 'time'   # logging mode - rotate: time or size
options.log_rotate_when = 'D'      # logging unit: S / M / H / D / W0 - W6
options.log_rotate_interval = 60   # logging interval: 60 seconds
options.logging = 'warning'  # logging level: debug/info/warning/error
options.parse_command_line()


if __name__ == "__main__":

    async def initialize_database():
        await Tortoise.init(db_url='sqlite://AsyncSpiderweb.sqlite3', modules={'models': ['model']})
        await Tortoise.generate_schemas()
        res = await Schedulers.filter(status=True)
        for i in res:
            schedulers.add_job(execute_task, i.mode, trigger_args=ast.literal_eval(i.timer), id=i.jid,
                               args=[i.project, i.spider, i.version, i.ssp,
                                     i.mode, i.timer, i.creator, i.status])

    app = Application(router, debug=options.debug)
    app.listen(port=options.port)
    schedulers.start()
    loop = ioloop.IOLoop.current()
    loop.run_sync(initialize_database)
    logging.info('Tornado server start on http://localhost:{port}, DEBUG is {debug}'
                 .format(port=options.port, debug=options.debug))
    loop.start()

