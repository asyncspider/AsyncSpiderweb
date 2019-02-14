import os
import sys
import hashlib
import asyncio
import logging
from datetime import datetime
from random import sample
from functools import wraps
import jwt
import pkg_resources
from asyncio.subprocess import PIPE
from uuid import uuid1

from tortoise.queryset import Q
from settings import secret, expire
from model import User


def make_md5(value):
    m = hashlib.md5()
    m.update(value.encode('utf8'))
    res = m.hexdigest()
    return res


def random_letters(minimum=97, maximum=123):
    letters = [chr(i) for i in range(minimum, maximum)]
    code = "".join(sample(letters, 6))
    return code


def authorization(func):
    """ authorization decorator for json web token and permission"""
    @wraps(func)
    async def wrapper(self, *arg, **kwargs):
        token = self.request.headers.get('Authorization')
        level = {'observer': 1, 'developer': 2, 'superuser': 3}
        handler_level = level.get(self.permission)
        if token:
            try:
                info = jwt.decode(token, secret, leeway=expire, options={'verify_exp': True})
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


def finishes(self, status: int, message: str):
    self.set_status(status)
    self.finish(message)


def writes(self, status: int, message: str):
    self.set_status(status)
    self.write(message)
    return None


async def get_spiders(project: str, version: str):
    """
    get spider list in scrapy egg
    """
    job = str(uuid1())
    process_obj = await asyncio.create_subprocess_exec(
        sys.executable, '-m', 'component.common.runner', 'list',
        project, version, job,
        stdout=PIPE, stderr=PIPE)
    # Wait for the subprocess exit and read one line of output.
    stdout, stderr = await process_obj.communicate()
    spiders = stdout.decode().rstrip().split('\n')
    return spiders


def activate_egg(egg_path):
    """ scrapy need activate egg """
    try:
        d = next(pkg_resources.find_distributions(egg_path))
    except StopIteration:
        raise ValueError("Unknown or corrupt egg")
    d.activate()
    settings_module = d.get_entry_info('scrapy', 'settings').module_name
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_module)


def get_user_from_jwt(token):
    info = jwt.decode(token, secret, leeway=expire, options={'verify_exp': True})
    username = info.get('username')
    return username


def timedelta_format(period):
    """timedelta to str for human
    :return: 9-days,18:08:15
    """
    value = period.total_seconds()
    minute, second = divmod(value, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    return "{day}-days, {hour}:{minute}:{second}".format(
        day=int(day), hour=int(hour), minute=int(minute), second=round(second, 2))


def prep_params(arguments: dict):
    """Processing the received parameters
    :return: tuple
    """
    params = {}
    for i in arguments.data.keys():
        if arguments[i].raw_data:
            params[i] = arguments[i].raw_data[0]
        elif arguments[i].default:
            params[i] = arguments[i].default
    ordering = params.pop('ordering')
    limit = params.pop('limit')
    offset = params.pop('offset')
    return params, offset, limit, ordering


class InsProtocol(asyncio.SubprocessProtocol):
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


async def ins_subprocess(target: str, operation: str, *args, **kwargs):
    """subprocess generated according to protocol settings execute specified files
    :param target: executable python file
    :param operation: crawl or list
    :return: a list, including runtime/stdout/stderr
    """
    spider, project, version, job = args[-4:]
    loop = asyncio.get_running_loop()
    exit_future = asyncio.Future(loop=loop)
    insp = lambda: InsProtocol(exit_future)
    transport, protocol = await loop.subprocess_exec(
        insp, sys.executable, '-m', target, operation, spider,
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


