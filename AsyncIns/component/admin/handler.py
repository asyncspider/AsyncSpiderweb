from datetime import datetime
from tornado.web import RequestHandler

import jwt
from tornado.httpclient import HTTPError
from tortoise.queryset import Q
from model import SuperUser, User, Permission, Role
from .forms import *
from ..common.util import make_md5, random_letters
from settings import secret


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
        res = await User.filter(Q(username=username) | Q(email=email))
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


class LoginHandler(RequestHandler):
    async def post(self, *args, **kwargs):
        users = LoginForm(self.request.arguments)
        if not users.validate(): raise HTTPError(400, message='params is error')
        username = users.username.data
        pwd = make_md5(users.password.data)
        code =users.code.data
        status = await User.filter(Q(username=username ) & Q(status=True))
        verify = await User.filter(Q(username=username) & Q(verify=True))

        if status:
            if verify:
                user = await User.filter(Q(username=username) & Q(password=pwd)).first()
            else:
                user = await User.filter(Q(username=username) &
                                         Q(password=pwd) &
                                         Q(code=code)).first()
                if user:
                    await User.filter(username=username).update(verify=True)
                else:
                    self.write('verify code incorrect')
            if user:
                payload = {'id': user.id, 'username': user.username, 'exp': datetime.utcnow()}
                token = jwt.encode(payload, secret, algorithm='HS256').decode('utf8')
                self.finish({'id': user.id,'username': user.username, "token": token})
            else:
                self.finish('username or password incorrect')
        else:
            self.finish('Account not activated')


class RoleHandler(RequestHandler):
    async def get(self, *args, **kwargs):
        role = await Role.all()
        item = {}
        for i in role:
            dps = i.permissions
            print(dps)
        item['count'] = len(role)
        item['data'] = [{'id': i.id, 'name': i.name, 'permissions': i.permissions,
                         'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
                        for i in role]
        self.finish(item)

    async def post(self, *args, **kwargs):
        role = RoleForm(self.request.arguments)
        if not role.validate(): raise HTTPError(400, message='params is error')
        name = role.name.data
        permissions = role.permissions.data
        per = await Permission.filter(name=permissions).count()
        if per:
            await Role.create(name=name, permissions=permissions)
        else:
            self.set_status(400)
        self.finish()

    async def put(self, *args, **kwargs):
        role = RoleForm(self.request.arguments)
        if not role.validate(): raise HTTPError(400, message='params is error')
        id = role.id.data
        name = role.name.data
        permissions = role.permissions.data
        await Role.filter(id=id).update(Q(name=name) & Q(permissions=permissions))

    async def delete(self, *args, **kwargs):
        role = RoleForm(self.request.arguments)
        if not role.validate(): raise HTTPError(400, message='params is error')
        id = role.id.data
        await Role.filter(id=id).delete()


