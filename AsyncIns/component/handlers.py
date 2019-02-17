import ast
import logging
from time import time
from tornado.web import RequestHandler
from apscheduler.jobstores.base import JobLookupError
from .forms import ProjectsForm, SchedulersForm, UserForm, LoginForm
from .parts import *
from .bases import RestfulHandler
from .executor.distribute import execute_task
from model import Projects, Schedulers, Records
from settings import schedulers, SECRET, ALGORITHM


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
        jobs = get_current_jobs(schedulers.get_jobs())
        response = dict(count=len(jobs))
        response['result'] = jobs
        self.finish(response)


class ProjectsHandler(RestfulHandler):

    storage = FileStorage()

    async def get(self, *args, **kwargs):
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
        params, offset, limit, ordering = prep(arguments)
        query = await Projects.filter(**params).offset(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['results'] = [
            {'id': i.id, 'project': i.project, 'spiders': i.spiders,
             'version': i.version, 'ssp': i.ssp, 'number': i.number,
             'filename': i.filename,  'creator': i.creator,
             'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
            for i in query]
        self.finish(response)

    async def post(self, *args, **kwargs):
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
        token = self.request.headers.get('Authorization')
        username = get_username(token)
        project = arguments.project.data
        ssp = arguments.ssp.data
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
        if not ssp:
            gross = await get_spider_list(project, version)
            spiders = ','.join(gross)
            number = len(gross)
        await Projects.create(project=project, spiders=spiders, version=version,
                              ssp=ssp, number=number, filename=filename, creator=username,
                              create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.over(201, {'spider': spiders, 'number': number, 'message': 'successful'})

    async def delete(self, *args, **kwargs):
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
        pid = arguments.id.data
        project = arguments.project.data
        version = arguments.version.data
        query = await Projects.filter(Q(id=pid) & Q(project=project) & Q(version=version))
        if query:
            try:
                await Projects.filter(id=pid).delete()
                result = self.storage.delete(self.storage.makepath(project, version))
                if result:
                    return self.over(200, {'project': project, 'version': version, 'message': 'successful'})
            except Exception as error:
                logging.warning(error)
        self.over(400, {'project': project, 'version': version, 'message': 'failed'})


class SchedulersHandler(RestfulHandler):

    async def get(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
        params, offset, limit, ordering = prep(arguments)
        query = await Schedulers.filter(**params).offset(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['current'] = get_current_jobs(schedulers.get_jobs())
        response['results'] = [
            {'id': i.id, 'jid': i.jid, 'project': i.project, 'spider': i.spider,
             'version': i.version, 'ssp': i.ssp, 'job': i.job,
             'mode': i.mode, 'timer': i.timer, 'status': i.status,
             'creator': i.creator, 'create_time': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
            for i in query]
        self.finish(response)

    async def post(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
        token = self.request.headers.get('Authorization')
        project = arguments.project.data
        version = arguments.version.data
        spider = arguments.spider.data
        ssp = arguments.ssp.data
        mode = arguments.mode.data
        username = get_username(token)
        # mode is interval, value {'seconds': 5}
        # mode is date, value {'run_date': '2019-02-13 17:05:05'}
        # mode is cron, value {'day_of_week': 'mon-fri', 'hour': 5, 'minute': 30, 'end_date': '2014-05-30'}
        try:
            timer = ast.literal_eval(arguments.timer.data)
        except Exception as error:
            logging.warning(error)
            return self.interrupt(400, 'error of timer')
        if not isinstance(timer, dict):
            return self.interrupt(400, 'error of timer')
        status = arguments.status.data
        jid = str(uuid1())  # scheduler job id, can remove job

        if status:
            schedulers.add_job(execute_task, mode, trigger_args=timer, id=jid,
                               args=[project, spider, version, ssp, mode,
                                     arguments.timer.data, username, status])
        await Schedulers.create(project=project, spider=spider, version=version,
                                ssp=ssp, mode=mode, timer=timer,
                                creator=username, status=status, jid=jid,
                                create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.over(201, {'project': project, 'version': version, 'status': status, 'message': 'successful'})

    async def put(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
        token = self.request.headers.get('Authorization')
        sid = arguments.id.data
        mode = arguments.mode.data
        username = get_username(token)
        status = arguments.status.data
        try:
            timer = ast.literal_eval(arguments.timer.data)
        except Exception as error:
            logging.warning(error)
            return self.interrupt(400, 'error of timer')
        query = await Schedulers.filter(id=sid).first()
        if not query:
            return self.interrupt(400, 'This scheduler dose not exist')
        try:
            if query.status and not status:  # cancel task according to status
                schedulers.remove_job(query.jid)
            if status and not query.status:  # add task according to status
                schedulers.add_job(execute_task, mode,
                                   trigger_args=timer, id=query.jid,
                                   args=[query.project, query.spider, query.version, mode, timer, username, status])
            if status and status == query.status:  # update task according to status
                schedulers.reschedule_job(query.jid, trigger=mode, trigger_args=timer)
            await Schedulers.filter(id=sid).update(mode=mode, timer=arguments.timer.data,
                                                   creator=username, status=status)
        except JobLookupError as error:
            logging.warning(error)
            await Schedulers.filter(id=sid).delete()
            return self.interrupt(reason='No job by the id of {jid} was found.'
                                  'This may be because the timer has expired, not a fatal error.'
                                  'The corresponding scheduler will be delete.'
                                  'Don\'t worry.'.format(jid=query.jid))
        self.finish({'project': query.project, 'version': query.version, 'status': status, 'message': 'successful'})

    async def delete(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
        sid = arguments.id.data
        query = await Schedulers.filter(id=sid).first()
        if not query:
            return self.interrupt(400, 'This scheduler dose not exist')
        try:
            schedulers.remove_job(query.jid)
        except JobLookupError as error:
            logging.warning(error)
        await Schedulers.filter(id=sid).delete()
        response = {'id': query.id, 'project': query.project, 'spider': query.spider,
                    'version': query.version, 'jid': query.jid, 'mode': query.mode,
                    'timer': query.timer, 'message': 'successful'}
        return self.over(200, response)


class RecordsHandler(RequestHandler):
    async def get(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
        params, offset, limit, ordering = prep(arguments)
        query = await Records.filter(**params).offset(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['results'] = [
            {'id': i.id, 'project': i.project, 'spider': i.spider,
             'version': i.version, 'ssp': i.ssp, 'job': i.job,
             'mode': i.mode, 'timer': i.timer, 'status': i.status,
             'start': i.start, 'end': i.end, 'period': i.period,
             'creator': i.creator, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
            for i in query]
        self.finish(response)


class RegisterHandler(RestfulHandler):

    async def post(self):
        arguments = UserForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
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
            return self.interrupt(400, 'failed of parameters validator')
        username = arguments.username.data
        pwd = make_md5(arguments.password.data)
        code = arguments.code.data
        user = await User.filter(Q(username=username) & Q(password=pwd)).first()
        if not user:
            return self.interrupt(400, 'username or password error')
        payload = {'id': user.id, 'username': user.username, 'exp': datetime.utcnow()}
        token = jwt.encode(payload, SECRET, ALGORITHM).decode('utf8')
        if user.role == 'superuser' or user.verify and user.status:
            return self.over(data={'id': user.id, 'username': user.username, 'token': token})
        superuser = await User.filter(role='superuser').first()
        if user.status and not user.verify:
            res = await User.filter(Q(username=username) & Q(password=pwd) & Q(code=code)).first()
            if res:
                await User.filter(Q(username=username) & Q(password=pwd) & Q(code=code)).update(verify=True)
                return self.over(data={'id': user.id, 'username': user.username, 'token': token})
            else:
                return self.interrupt(400,
                                      'verify code error, '
                                      'please contact the superuser:{username}(email:{email})'
                                      .format(username=superuser.username, email=superuser.email))
        return self.interrupt(400,
                              'user status is false,'
                              'please contact the superuser:{username}(email:{email})'
                              .format(username=superuser.username, email=superuser.email))


class UserHandler(RestfulHandler):

    async def get(self):
        arguments = UserForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
        params, offset, limit, ordering = prep(arguments)
        query = await User.filter(**params).offset(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['results'] = [
            {'id': i.id, 'username': i.username, 'status': i.status,
             'verify': i.verify, 'code': i.code, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
            for i in query]
        self.finish(response)

    async def put(self, *args, **kwargs):
        arguments = LoginForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
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
        self.finish({'message': 'successful'})

    async def delete(self, *args, **kwargs):
        arguments = LoginForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failed of parameters validator')
        user_id = arguments.id.data
        query = await User.filter(id=user_id).first()
        if not query:
            return self.interrupt(400, 'user dose not exist')
        await User.filter(id=user_id).delete()
        self.over(200, {'message': 'successful'})


