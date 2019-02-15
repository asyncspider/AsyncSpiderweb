import ast
import logging
from time import time
from tornado.web import RequestHandler
from model import *
from .validators import ProjectsForm, SchedulersForm, RecordsForm, UserForm, RegisterForm, LoginForm
from .parts import *
from .executor.distribute import execute_task
from model import Projects, Schedulers, Records
from settings import schedulers


class RestfulHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Access-Control-Allow-Origin,'
                        'Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def interrupt(self, status_code: int = 200, reason='Response was forced to interrupt'):
        resp = dict(message=reason)
        if isinstance(resp, dict):
            self.set_status(status_code)
            self.write(resp)

    def over(self, status_code: int = 200, data: dict = {'message': 'Response was finish'}):
        self.set_status(status_code)
        self.write(data)
        self.finish()


class IndexHandler(RestfulHandler):
    permission = 'observer'

    # @authorization
    # async def get(self, *args, **kwargs):
    #     sec = int(self.request.arguments.get('sec')[0])
    #     schedulers.add_job(traversal_queue, 'interval', seconds=sec, max_instances=10)

    # async def get(self, *args, **kwargs):
    #     print('this is index handler')
    #     data = await get_spider_list('arts', '1550036771')
    #     logging.warning(data)

    async def get(self, *args, **kwargs):
        self.finish({'message': 'index'})


class ProjectsHandler(RestfulHandler):

    storage = FileStorage()

    async def get(self, *args, **kwargs):
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        params, offset, limit, ordering = prep(arguments)
        query = await Projects.filter(**params).offset(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['data'] = [
            {'id': i.id, 'project': i.project, 'spiders': i.spiders,
             'version': i.version, 'custom': i.custom, 'spider_num': i.spider_num,
             'egg': i.egg_path, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
            for i in query]
        self.finish(response)

    async def post(self, *args, **kwargs):
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        token = self.request.headers.get('Authorization')
        username = get_username(token) if token else None
        project = arguments.project.data
        ins = arguments.ins.data
        spiders = project
        number = 1
        eggs = self.request.files.get('eggs')
        version = str(round(time()))
        if not all([eggs, project, version]):
            return self.interrupt(400, 'missing parameters')
        egg = eggs.pop()
        filename = egg['filename']
        if not filename.endswith('.egg'):
            return self.interrupt(400, 'file is not egg')
        filename = await self.storage.put(egg['body'], project, version)
        if not ins:
            gross = await get_spider_list(project, version)
            spiders = ','.join(gross)
            number = len(gross)
        await Projects.create(project=project, spiders=spiders, version=version,
                              ins=ins, number=number, filename=filename, creator=username,
                              create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.over(201, {'spider': spiders, 'number': number})

    async def delete(self, *args, **kwargs):
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        sid = arguments.id.data
        project = arguments.project.data
        version = arguments.version.data
        await Projects.filter(id=sid).delete()
        await self.storage.delete(project, version)
        self.over(204, {'project': project, 'version': version})


class SchedulersHandler(RestfulHandler):

    async def get(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        params, offset, limit, ordering = prep(arguments)
        query = await Schedulers.filter(**params).offse(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['data'] = [
            {'id': i.id, 'project': i.project, 'spider': i.spider,
             'version': i.version, 'ins': i.ins, 'job': i.job,
             'mode': i.mode, 'timer': i.timer, 'status': i.status,
             'creator': i.creator, 'create_time': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
            for i in query]
        self.finish(response)

    async def post(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        token = self.request.headers.get('Authorization')
        project = arguments.project.data
        version = arguments.version.data
        spider = arguments.spider.data
        ins = arguments.ins.data
        mode = arguments.mode.data
        username = get_username(token) if token else None
        # mode is interval, value {'seconds': 5}
        # mode is date, value {'run_date': '2019-02-13 17:05:05'}
        # mode is cron, value {'day_of_week': 'mon-fri', 'hour': 5, 'minute': 30, 'end_date': '2014-05-30'}
        timer = ast.literal_eval(arguments.timer.data)
        status = arguments.status.data
        jid = str(uuid1())  # scheduler job id, can remove job
        await Schedulers.create(project=project, spider=spider, version=version,
                                ins=ins, mode=mode, timer=timer,
                                creator=username, status=status, jid=jid,
                                create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if status:
            schedulers.add_job(execute_task, mode, trigger_args=timer, id=jid,
                               args=[project, spider, version, ins, mode, arguments.timer.data, username, status])
        self.over(201, {'project': project, 'version': version, 'status': status})

    async def put(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        token = self.request.headers.get('Authorization')
        sid = arguments.id.data
        version = arguments.version.data
        mode = arguments.mode.data
        username = get_username(token) if token else None
        status = arguments.status.data
        try:
            timer = ast.literal_eval(arguments.timer.data)
        except Exception as err:
            return self.interrupt(400, err)
        query = await Schedulers.filter(id=sid).first()
        if query.status and not status:  # cancel task according to status
            try:
                schedulers.remove_job(query.jid)
            except Exception as err:
                return self.interrupt(400, err)
        if status and not query.status:  # add task according to status
            schedulers.add_job(execute_task, mode,
                               trigger_args=timer, id=query.jid,
                               args=[query.project, query.spider, version, mode, timer, username, status])
        await Schedulers.filter(id=sid).update(mode=mode, timer=arguments.timer.data,
                                               creator=username, status=status)
        self.finish({'project': query.project, 'version': version, 'status': status})


class RecordsHandler(RequestHandler):
    async def get(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        params, offset, limit, ordering = prep(arguments)
        query = await Records.filter(**params).offset(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['data'] = [
            {'id': i.id, 'project': i.project, 'spider': i.spider,
             'version': i.version, 'ins': i.ins, 'job': i.job,
             'mode': i.mode, 'timer': i.timer, 'status': i.status,
             'start': i.start, 'end': i.end, 'period': i.period,
             'creator': i.creator, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
            for i in query]
        self.finish(response)


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
        code = random_characters(n=6)
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
        response['data'] = [
            {'id': i.id, 'username': i.username, 'status': i.status,
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


