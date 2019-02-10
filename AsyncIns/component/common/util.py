import hashlib
from random import sample
from functools import wraps
import jwt

from tortoise.queryset import Q
from settings import secret, expire
from model import User

def make_md5(value):
    m = hashlib.md5()
    m.update(value.encode('utf8'))
    res = m.hexdigest()
    return res

def random_letters(min=97, max=123):
    letters = [chr(i) for i in range(min, max)]
    code = "".join(sample(letters, 6))
    return code


def authorization(func):
    """ authorization decorator for json web token"""
    @wraps(func)
    async def wrapper(self, *arg, **kwargs):
        token = self.request.headers.get('Authorization')
        if token:
            try:
                info = jwt.decode(token, secret, leeway=expire, options={'verify_exp': True})
                id = info.get('id')
                username = info.get('username')
                user = await User.filter(Q(id=id) & Q(username=username))
                if user:
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
