import os
import sys
import hashlib
import asyncio
import logging
import pkg_resources
from datetime import datetime, timedelta
from os import path, remove
from random import sample
from functools import wraps
from uuid import uuid1
from asyncio.subprocess import PIPE


import jwt
import aiofiles

from settings import EGG_DIR, TEMP_DIR, SECRET, EXPIRE, EXECUTOR_PILOT, DEFAULT_OFFSET
from tortoise.queryset import Q
from model import User


# Simple Work. For example: something path, format conversion and other work.


def str_to_hash(value: str):
    if isinstance(value, str):
        m = hashlib.md5()
        m.update(value.encode('utf8'))
        return m.hexdigest()
    raise ValueError('Parameter must be str')


def random_characters(minimum: int = 97, maximum: int = 123, n: int = 6):
    """ Generate n random characters base on ascii
    :param minimum: ascii code
    :param maximum: ascii code
    :param n: number
    :return: random characters of length n, for example 'flower'
    """
    if all([isinstance(minimum, int), isinstance(maximum, int), isinstance(n, int)]):
        if maximum - minimum >= n:
            letters = [chr(i) for i in range(minimum, maximum)]
            code = "".join(sample(letters, n))
            return code
        raise ValueError('{max} - {min} >= {n}'.format(max=maximum, min=minimum, n=n))
    raise TypeError('Parameter must be int')


async def get_spider_list(project: str, version: str):
    """ Get spider list from scrapy egg """
    if isinstance(version, str):
        process_obj = await asyncio.create_subprocess_exec(
            sys.executable, '-m', EXECUTOR_PILOT, 'list',
            project, version, str(uuid1()),
            stdout=PIPE, stderr=PIPE)
        stdout, stderr = await process_obj.communicate()  # Wait for the subprocess exit and read one line of output.
        spiders = stdout.decode().rstrip().split('\n')
        return spiders
    raise TypeError('version must be str')


def activate_egg(egg_path):
    """ Scrapy project needs to be activated before running """
    try:
        d = next(pkg_resources.find_distributions(egg_path))
    except StopIteration:
        raise ValueError("Unknown or corrupt egg")
    d.activate()
    settings_module = d.get_entry_info('scrapy', 'settings').module_name
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_module)


def get_username(token: str):
    """ Get username from json web token """
    if token:
        info = jwt.decode(token, SECRET, leeway=EXPIRE, options={'verify_exp': True})
        username = info.get('username')
        return username
    return None


def timedelta_format(period: timedelta):
    """ Timedelta to str for human
    :period: timedelta
    :return: str, for example '5-days,18:08:15'
    """
    if isinstance(period, timedelta):
        value = period.total_seconds()
        minute, second = divmod(value, 60)
        hour, minute = divmod(minute, 60)
        day, hour = divmod(hour, 24)
        return "{day}-days, {hour}:{minute}:{second}".format(
            day=int(day), hour=int(hour), minute=int(minute), second=round(second, 2))
    raise TypeError('Parameter period must be timedelta')


def prep(arguments: object, threshold: int = DEFAULT_OFFSET):
    """ Filtering and classification of parameters """
    if not all([isinstance(arguments, object), isinstance(threshold, int)]):
        raise TypeError('Parameter type error')
    params = {}
    try:
        for i in arguments.data.keys():
            if arguments[i].raw_data:
                params[i] = arguments[i].raw_data[0]
            elif arguments[i].default:
                params[i] = arguments[i].default
        ordering = params.pop('ordering')
        limit = params.pop('limit')
        offset = params.pop('offset')
        if offset == threshold:
            offset = 0
        return params, offset, limit, ordering
    except Exception as err:
        raise AttributeError(err)


def get_current_jobs(jobs: object):
    """Get current job and format the args
    :param jobs: apscheduler Job object list
    :return: job list
    """
    result, des = [], {}
    for i in jobs:
        des['jid'] = i.id
        des['func'] = i.func_ref
        des['project'], des['spider'], des['version'], des['ssp'], des['mode'], \
        des['timer'], des['creator'], des['status'] = i.args
        result.append(des)
    return result


def authorization(func):
    """ user authentication and permission decorator"""
    @wraps(func)
    async def wrapper(self, *arg, **kwargs):
        token = self.request.headers.get('Authorization')
        level = {'observer': 1, 'developer': 2, 'superuser': 3}
        handler_level = level.get(self.permission)
        if token:
            try:
                info = jwt.decode(token, SECRET, leeway=EXPIRE, options={'verify_exp': True})
                user_id = info.get('id')
                username = info.get('username')
                user = await User.filter(Q(id=user_id) & Q(username=username))
                user_role = level.get(user.role)
                if user and user_role >= handler_level:
                    self._current_user = user
                    await func(self, *arg, **kwargs)
                else:
                    self.set_status(401)
            except Exception as error:
                self.set_status(401)
        else:
            self.set_status(401)
        self.finish()
    return wrapper


# Complex Work.


async def async_subprocess(target: str, operation: str, *args, **kwargs):
    """ subprocess generated according to protocol settings execute specified files for run scrapy egg
    :param target: name of executable python file
    :param operation: 'crawl' or 'list'
    :return: scrapy egg running information
    """
    spider, project, version, job = args[-4:]
    loop = asyncio.get_running_loop()
    exit_future = asyncio.Future(loop=loop)
    async_sub = lambda: AsyncSubprocessProtocol(exit_future)
    transport, protocol = await loop.subprocess_exec(
        async_sub, sys.executable, '-m', target, operation, spider,
        project, version, job,
        stdin=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE)
    await exit_future
    transport.close()
    std = bytes(protocol.output).decode('ascii').rstrip()
    period = timedelta_format(protocol.end - protocol.start)
    return [protocol.start.strftime('%Y-%m-%d %H:%M:%S'),
            protocol.end.strftime('%Y-%m-%d %H:%M:%S'),
            period, std]


class AsyncSubprocessProtocol(asyncio.SubprocessProtocol):
    """ Set subprocess protocol according to requirement """
    def __init__(self, exit_future):
        self.exit_future = exit_future
        self.output = bytearray()
        self.start = None
        self.end = None

    def connection_made(self, transport):
        self.start = datetime.now()

    def pipe_data_received(self, fd, data):
        self.output.extend(data)

    def process_exited(self):
        self.end = datetime.now()
        self.exit_future.set_result(True)


class FileStorage:

    def __init__(self):
        self.dirs = EGG_DIR

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
        try:
            remove(file_path)
            return True
        except Exception as error:
            logging.warning(error)
            return False

    async def copy_to_temp(self, project, version, temp=TEMP_DIR, job=None):
        storage_egg = self.makepath(project, version)
        temp_egg = self.makepath(project, version, temp, job)
        async with aiofiles.open(storage_egg, 'rb') as f:
            content = await f.read()
        async with aiofiles.open(temp_egg, 'wb') as f:
            await f.write(content)
        return temp_egg

    async def exists(self, project, version):
        filename = self.makepath(project, version)
        try:
            async with aiofiles.open(filename, 'w') as f:
                await f.close()
            return True
        except Exception as err:
            logging.warning(err)
            return False

    def makepath(self, project, version, file_path=None, job=None):
        if not file_path:
            file_path = self.dirs
        if job:
            return path.join(file_path, "{job}.egg".format(job=job))
        return path.join(file_path, "{project}_{version}.egg".format(project=project, version=version))

