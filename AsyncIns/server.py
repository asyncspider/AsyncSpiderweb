from tornado.web import Application
from tornado import ioloop
from tornado.options import options, define


from urls import router
from tortoise import Tortoise
from component.scheduler.tasks import traversal_queue
from settings import schedulers

# define 定义一些可以在命令行中传递的参数以及类型
define('port', default=8000, help='run on the given port', type=int)
define('debug', default=True, help='set tornado debug mode', type=bool)
options.parse_command_line()


if __name__ == "__main__":
    async def run():
        await Tortoise.init(db_url='sqlite://octopus.sqlite3', modules={'models': ['model']})
        await Tortoise.generate_schemas()

    app = Application(router, debug=options.debug)
    app.listen(port=options.port)
    schedulers.add_job(traversal_queue, 'interval', seconds=3)
    schedulers.start()
    loop = ioloop.IOLoop.current()
    loop.run_sync(run)
    loop.start()

