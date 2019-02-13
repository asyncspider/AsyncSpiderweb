from os import path, remove


import aiofiles
from settings import storage_dir, temp_dir
from ..common.util import activate_egg


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

    def delete(self, file_path):
        remove(file_path)

    async def copy_to_temp(self, project, version, temp=temp_dir):
        storage_egg = self.makepath(project, version)
        temp_egg = self.makepath(project, version, temp)
        async with aiofiles.open(storage_egg, 'rb') as f:
            content = await f.read()
        async with aiofiles.open(temp_egg, 'wb') as f:
            await f.write(content)
        return temp_egg

    def makepath(self, project, version, file_path=None):
        """return: project_15409890987.egg
        """
        if not file_path:
            file_path = self.storage_dir
        return path.join(file_path, "{project}_{version}.egg".format(project=project, version=version))

    async def exists(self, project, version):
        """ does the file exists"""
        filename = self.makepath(project, version)
        try:
            async with aiofiles.open(filename, 'w') as f:
                await f.close()
            return True
        except Exception as error:
            return False
