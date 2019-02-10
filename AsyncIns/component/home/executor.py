import sys
import importlib
from datetime import datetime

from tornado import ioloop
from tornado.gen import coroutine
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from component.home.storage import FileStorage



class Environment:
    executor = ThreadPoolExecutor(2)

    def __init__(self, project, spider, version):
        self.storage = FileStorage()
        self.project = project
        self.spider = spider
        self.version = version
        self.file_path = '/home/gannicus/github/EggTest/projects/demo1/hello-1.0-py3.7.egg' # self.storage.makepath(self.project, self.version)

    async def __aenter__(self):
        """ prepare """
        exists = await self.storage.exists(self.project, self.version)
        assert exists, "Egg does not exist"
        sys.path.append(self.file_path)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @coroutine
    def execs(self):
        """ make synchronous operations asynchronous  """
        start = yield self.runner()
        end = datetime.now()
        print('run time:')
        print(end-start)

    async def ecs(self):
        ioloop.IOLoop.instance().add_callback(self.runner)
        print('ecs')

    @run_on_executor
    def runner(self):
        """ run the specified project  """
        start = datetime.now()
        module = importlib.import_module('hello')
        print(start)
        module.run()
        print(datetime.now())



# if __name__ == "__main__":
#     import asyncio
#
#     async def run():
#         async with Environment() as eir:
#             await eir.runner()
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(run())
#
# if __name__ == "__main__":
#     # paths = FileStorage().makepath('hello', '1500000000000')
#     # sys.path.append(paths)
#     # module = importlib.import_module('hello')
#     import sys
#     import importlib
#     sys.path.append('/home/gannicus/PycharmProjects/octopus/filestorage/hello_1500000000000.egg')
#
#     module = importlib.import_module('hello')
#     module.run()


