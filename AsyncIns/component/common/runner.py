import sys
import os
import shutil
import tempfile
from contextlib import contextmanager

from scrapyd import get_application
from scrapyd.interfaces import IEggStorage
from scrapyd.eggutils import activate_egg


import importlib
from datetime import datetime
import aiofiles
from tornado import ioloop
from tornado.gen import coroutine
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from component.home.storage import FileStorage


class Environment(object):
    executor = ThreadPoolExecutor(2)

    def __init__(self, project, version):
        self.storage = FileStorage()
        self.project = project
        self.version = version
        self.file_path = self.storage.makepath(self.project, self.version)

    async def __aenter__(self):
        self.temp_egg = self.storage.copy_to_temp(self.project, self.version)
        activate_egg(self.temp_egg)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.temp_egg:
            self.storage.delete(self.temp_egg)


def main():
    project, version = os.environ['SCRAPY_PROJECT'], os.environ['SCRAPY_VERSION']
    async with Environment(project, version):
        from scrapy.cmdline import execute
        execute()


if __name__ == '__main__':
    main()
