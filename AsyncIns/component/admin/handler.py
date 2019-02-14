from datetime import datetime
from tornado.web import RequestHandler
import jwt
from tortoise.queryset import Q
from model import User
from .forms import *
from ..common.util import make_md5, random_letters, finishes, prep_params
from settings import secret


class RegisterHandler(RequestHandler):

    async def post(self):
        arguments = UserForm(self.request.arguments)
        # if not arguments.validate():
        #     finishes(self, 400, 'field validators error')
        #     return None
        username = arguments.username.data
        email = arguments.email.data
        role = arguments.role.data
        res = await User.filter(Q(username=username) | Q(email=email))
        if role == 'superuser':
            superuser_exits = await User.filter(role='superuser').count()
            if superuser_exits:
                finishes(self, 400, 'superuser is exits')
                return None
        if res:
            finishes(self, 400, 'username or email exits')
            return None
        password = arguments.password.data
        pwd = make_md5(password)
        code = random_letters()
        await User.create(username=username, password=pwd, email=email, code=code, role=role)
        finishes(self, 201, 'registration successful：{username} '.format(username=username))


class LoginHandler(RequestHandler):
    async def post(self, *args, **kwargs):
        arguments = LoginForm(self.request.arguments)
        if not arguments.validate():
            finishes(self, 400, 'field validators error')
            return None
        username = arguments.username.data
        pwd = make_md5(arguments.password.data)
        code = arguments.code.data
        user = await User.filter(Q(username=username) & Q(password=pwd)).first()
        if not user:
            finishes(self, 400, 'username or password error')
            return None
        payload = {'id': user.id, 'username': user.username, 'exp': datetime.utcnow()}
        token = jwt.encode(payload, secret, algorithm='HS256').decode('utf8')
        if user.role == 'superuser' or user.verify and user.status:
            finishes(self, 200, {'id': user.id, 'username': user.username, 'token': token})
            return None
        if user.status and not user.verify:
            res = await User.filter(Q(username=username) & Q(password=pwd) & Q(code=code)).first()
            if res:
                await User.filter(Q(username=username) & Q(password=pwd) & Q(code=code)).update(verify=True)
                finishes(self, 200, {'id': user.id, 'username': user.username, 'token': token})
            else:
                finishes(self, 400, 'verify code error')
        else:
            finishes(self, 400, 'user status is false')


class UserHandler(RequestHandler):
    async def get(self):
        arguments = UserForm(self.request.arguments)
        # if not arguments.validate():
        #     finishes(self, 400, 'field validators error')
        #     return None
        params, offset, limit, ordering = prep_params(arguments)
        query = await User.filter(**params).offset(offset).limit(limit).order_by(ordering)
        item = dict(count=len(query))
        item['data'] = [{'id': i.id, 'username': i.username, 'status': i.status,
                         'verify': i.verify, 'code': i.code, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
                        for i in query]
        finishes(self, 200, item)

    async def put(self, *args, **kwargs):
        arguments = LoginForm(self.request.arguments)
        if not arguments.validate():
            finishes(self, 400, 'field validators error')
            return None
        params, offset, limit, ordering = prep_params(arguments)
        uid = params.pop('id')
        # user_id = arguments.id.data
        # status = arguments.status.data
        # password = arguments.password.data
        res = await User.filter(id=uid).update(**params)
        # if all([user_id, status, password]):
        #     res = await User.filter(id=user_id).update(Q(status=status) & Q(password=password))
        # elif user_id and status:
        #     res = await User.filter(id=user_id).update(status=status)
        # elif user_id and password:
        #     res = await User.filter(id=user_id).update(password=password)
        finishes(self, 200, 'update successful') if res else finishes(self, 400, 'delete failed')

    async def delete(self, *args, **kwargs):
        arguments = LoginForm(self.request.arguments)
        if not arguments.validate():
            finishes(self, 400, 'field validators error')
            return None
        user_id = arguments.id.data
        res = await User.filter(id=user_id).delete()
        finishes(self, 200, 'delete successful') if res else finishes(self, 400, 'delete failed')

