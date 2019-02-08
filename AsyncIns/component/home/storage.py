from os import path, remove


import aiofiles
from settings import storage_dir


class FileStorage(object):

    def __init__(self):
        self.storage_dir = storage_dir

    async def get(self, project, version):
        async with aiofiles.open(self.makepath(project, version), 'rb') as f:
            file = await f.read()
        return file

    async def put(self, file, project, version):
        file_path = self.makepath(project, version)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file)
        return "{project}_{version}.egg".format(project=project, version=version)

    async def delete(self, project, version):
        remove(self.makepath(project, version))

    def makepath(self, project, version):
        """
        return: arts_15409890987.egg
        """
        return path.join(self.storage_dir, "{project}_{version}.egg".format(project=project, version=version))

    async def exists(self, project, version):
        """ does the file exists"""
        filename = self.makepath(project, version)
        try:
            async with aiofiles.open(filename, 'w') as f:
                await f.close()
            return True
        except Exception as error:
            return False
