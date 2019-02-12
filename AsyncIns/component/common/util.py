import os
import sys
import hashlib
import asyncio
from random import sample
from functools import wraps
import jwt
import pkg_resources
from asyncio.subprocess import PIPE

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
                id = info.get('id')
                username = info.get('username')
                user = await User.filter(Q(id=id) & Q(username=username))
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


def finish_resp(self, status: int, message: str):
    self.set_status(status)
    self.finish(message)


async def get_scrapy_spiders(project, version):
    """ get spider list in egg """
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'UTF-8'
    env['SCRAPY_PROJECT'] = project
    env['SCRAPY_VERSION'] = version
    process_obj = await asyncio.create_subprocess_exec(
        sys.executable, '-m', 'runner', 'list', stdout=PIPE, stderr=PIPE)
    stdout, stderr = await process_obj.communicate()  # Wait for the subprocess exit and read one line of output.
    spiders = stdout.decode(stdout).rstrip()
    return "".join(spiders)


def activate_egg(egg_path):
    """ scrapy need activate egg """
    try:
        d = next(pkg_resources.find_distributions(egg_path))
    except StopIteration:
        raise ValueError("Unknown or corrupt egg")
    d.activate()
    settings_module = d.get_entry_info('scrapy', 'settings').module_name
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_module)

