from datetime import datetime
import jwt
from tortoise.queryset import Q
from model import User
from .forms import *
from ..common.util import make_md5, random_letters, finishes, prep
from settings import secret
from ..common.handler import RestfulHandler


class RegisterHandler(RestfulHandler):

    async def post(self):
        arguments = UserForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        username = arguments.username.data
        email = arguments.email.data
        role = arguments.role.data
        password = arguments.password.data
        pwd = make_md5(password)
        code = random_letters()
        if role == 'superuser':
            superuser_exits = await User.filter(role='superuser').count()
            if superuser_exits:
                return self.interrupt(400, 'superuser is exist')
        res = await User.filter(Q(username=username) | Q(email=email))
        if res:
            return self.interrupt(400, 'username or email is exist')
        await User.create(username=username, password=pwd, email=email, code=code, role=role)
        self.over(201, {'message': 'welcome：{username} '.format(username=username)})


class LoginHandler(RestfulHandler):
    async def post(self, *args, **kwargs):
        arguments = LoginForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        username = arguments.username.data
        pwd = make_md5(arguments.password.data)
        code = arguments.code.data
        user = await User.filter(Q(username=username) & Q(password=pwd)).first()
        if not user:
            return self.interrupt(400, 'username or password error')
        payload = {'id': user.id, 'username': user.username, 'exp': datetime.utcnow()}
        token = jwt.encode(payload, secret, algorithm='HS256').decode('utf8')
        if user.role == 'superuser' or user.verify and user.status:
            return self.over(data={'id': user.id, 'username': user.username, 'token': token})
        if user.status and not user.verify:
            res = await User.filter(Q(username=username) & Q(password=pwd) & Q(code=code)).first()
            if res:
                await User.filter(Q(username=username) & Q(password=pwd) & Q(code=code)).update(verify=True)
                return self.over(data={'id': user.id, 'username': user.username, 'token': token})
            else:
                return self.interrupt(400, 'verify code error')
        return self.interrupt(400, 'user status is false')


class UserHandler(RestfulHandler):

    async def get(self):
        arguments = UserForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        params, offset, limit, ordering = prep(arguments)
        query = await User.filter(**params).offset(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['data'] = [{'id': i.id, 'username': i.username, 'status': i.status,
                            'verify': i.verify, 'code': i.code, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
                            for i in query]
        self.finish(response)

    async def put(self, *args, **kwargs):
        arguments = LoginForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        uid = arguments.id.data
        password = make_md5(arguments.password.data) if len(arguments.password.data) > 5 else None
        status = arguments.status.data
        email = arguments.email.data
        query = await User.filter(id=uid).first()
        if not query:
            return self.interrupt(400, 'user dose not exist')
        params = {}
        if all([email, len(email) > 5, email != query.email]):
            params['email'] = email
        if password != query.password and password:
            params['password'] = password
        if all([status, isinstance(status, bool), status != query.status]):
            params['status'] = status
        await User.filter(id=uid).update(**params)
        self.finish({'message': 'update successful'})

    async def delete(self, *args, **kwargs):
        arguments = LoginForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        user_id = arguments.id.data
        await User.filter(id=user_id).delete()
        self.over(204, {'message': 'delete successful'})

