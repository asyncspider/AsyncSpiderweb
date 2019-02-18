import sys
from tornado import ioloop
from ..parts import FileStorage, activate_egg


class Environment(object):

    def __init__(self, project, version, job):
        self.storage = FileStorage()
        self.project = project
        self.version = version
        self.job = job
        self.file_path = self.storage.makepath(self.project, self.version)

    async def __aenter__(self):
        self.temp_egg = await self.storage.copy_to_temp(project=self.project,
                                                        version=self.version,
                                                        job=self.job)

        activate_egg(self.temp_egg)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.temp_egg:
            self.storage.delete(self.temp_egg)


async def main():
    project, version, job = sys.argv[-3:]
    sys.argv = sys.argv[:3]
    async with Environment(project, version, job):
        from scrapy.cmdline import execute
        execute()


if __name__ == '__main__':
    loop = ioloop.IOLoop.instance()
    loop.run_sync(main)
