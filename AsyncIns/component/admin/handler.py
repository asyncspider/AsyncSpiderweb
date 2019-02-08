from random import randint
from tornado.web import RequestHandler

from tornado.httpclient import HTTPError
from tortoise.queryset import Q
from model import SuperUser, User
from .forms import SuperUserForm, CreateUserForm
from ..common.util import make_md5, random_letters


class SuperUserRegHandler(RequestHandler):
    async def post(self):
        res = await SuperUser.filter(verify=1).count()
        if res:
            self.set_status(400)
            self.finish('superuser exits')
        else:
            reg = SuperUserForm(self.request.arguments)
            if not reg.validate(): raise HTTPError(400, message='params is error')
            username = reg.username.data
            password = reg.password.data
            email = reg.email.data
            pwd = make_md5(password)
            await SuperUser.create(username=username, password=pwd, email=email, verify=True)


class CreateUserHandler(RequestHandler):

    async def get(self):
        users = CreateUserForm(self.request.arguments)
        if users.validate():
            order = users.order.data
            limit = users.limit.data
        res = await User.filter().limit(limit).order_by(order)
        item = {}
        item['count'] = len(res)
        item['data'] = [{'id': i.id, 'username': i.username, 'status': i.status,
                         'verify': i.verify, 'code': i.code, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
                        for i in res]
        self.finish(item)

    async def post(self):
        register = CreateUserForm(self.request.arguments)
        if not register.validate(): raise HTTPError(400, message='params is error')
        username = register.username.data
        email = register.email.data
        res = await User.filter(Q(username=username) | Q(email=email)).count()
        if res:
            self.set_status(400)
            self.finish('username or email exits')
        else:
            password = register.password.data
            pwd = make_md5(password)
            code = random_letters()
            await User.create(username=username, password=pwd, email=email, code=code)

    async def put(self, *args, **kwargs):
        users = CreateUserForm(self.request.arguments)
        if not users.validate(): raise HTTPError(400, message='params is error')
        id = users.id.data
        status = users.status.data
        await User.filter(id=id).update(status=status)

    async def delete(self, *args, **kwargs):
        users = CreateUserForm(self.request.arguments)
        if not users.validate(): raise HTTPError(400, message='params is error')
        id = users.id.data
        await User.filter(id=id).delete()
