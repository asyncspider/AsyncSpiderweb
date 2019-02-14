from os import path
from tornado.web import Application
from tornado import ioloop
from tornado.options import options, define

from urls import router
from tortoise import Tortoise
from settings import schedulers

# define 定义一些可以在命令行中传递的参数以及类型
define('port', default=8205, help='run on the given port', type=int)
define('debug', default=True, help='set tornado debug mode', type=bool)
options.log_file_prefix = path.join(path.dirname(__file__), 'logs/tornados/tornado.log')  # logs path
options.log_rotate_mode = 'time'   # logging mode - rotate: time or size
options.log_rotate_when = 'D'      # logging unit: S / M / H / D / W0 - W6
options.log_rotate_interval = 60   # logging interval: 60 seconds
options.logging = 'warning'  # logging level: debug info warning error
options.parse_command_line()


if __name__ == "__main__":
    async def run():

        await Tortoise.init(db_url='sqlite://AsyncIns.sqlite3', modules={'models': ['model']})
        await Tortoise.generate_schemas()

    app = Application(router, debug=options.debug)
    app.listen(port=options.port)
    schedulers.start()
    loop = ioloop.IOLoop.current()

    loop.run_sync(run)
    loop.start()

