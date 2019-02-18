import ast
import logging
from time import time
from tornado.web import RequestHandler
from apscheduler.jobstores.base import JobLookupError
from .forms import *
from .parts import *
from .bases import RestfulHandler
from .executor.distribute import execute_task
from model import Projects, Schedulers, Records
from settings import schedulers, SECRET, ALGORITHM


"""
    @apiDefine Operations
    @apiParam {Number} [limit=LIMIT_DEFAULT]   Optional Limit with default LIMIT_DEFAULT.
    @apiParam {String} [ordering='id']  Optional Ordering default 'id'.
    @apiParam {Number} [offset=OFFSET_DEFAULT]   Optional Limit with default OFFSET_DEFAULT.
    @apiParam {String} [fieldname]  filter field.
"""
"""
    @apiDefine ErrorExamples
    @apiErrorExample {json} Error-Response:
            HTTP/1.1 400 OK
            {'message': 'failed of parameters validator'}
"""


class IndexHandler(RestfulHandler):

    # @authorization
    # async def get(self, *args, **kwargs):
    #     sec = int(self.request.arguments.get('sec')[0])
    #     schedulers.add_job(traversal_queue, 'interval', seconds=sec, max_instances=10)

    # async def get(self, *args, **kwargs):
    #     print('this is index handler')
    #     data = await get_spider_list('arts', '1550036771')
    #     logging.warning(data)
    permission = 'observer'

    async def get(self, *args, **kwargs):
        """
        @apiGroup Index-get
        @apiPermission Observer
        @api {get} /
        @apiHeader {String} Authorization json web token
        @apiUse Operations
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "first name": "John",
            "last name": "Doe"
        }
        """
        jobs = get_current_jobs(schedulers.get_jobs())
        response = dict(count=len(jobs))
        response['result'] = jobs
        await self.over(data=response)


class ProjectsHandler(RestfulHandler):

    permission = 'developer'
    storage = FileStorage()

    async def get(self, *args, **kwargs):
        """
        @apiGroup Projects-get
        @apiPermission Developer
        @api {get} /projects/
        @apiHeader {String} Authorization json web token
        @apiUse Operations
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {'id': 1, 'project': 'arts', 'spiders': 'keeper, facts, hydra',
             'version': 1560326985623, 'ssp': false, 'number': 3,
             'filename': 'arts_1560326985623.egg,  'creator': 'username',
             'create': 2019-02-22 10:00:00}
        """
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
        params, offset, limit, ordering = prep(arguments)
        query = await Projects.filter(**params).offset(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['results'] = [
            {'id': i.id, 'project': i.project, 'spiders': i.spiders,
             'version': i.version, 'ssp': i.ssp, 'number': i.number,
             'filename': i.filename,  'creator': i.creator,
             'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
            for i in query]
        await self.over(data=response)

    async def post(self, *args, **kwargs):
        """
        @apiGroup Projects-post
        @apiPermission Developer
        @api {post} /projects/
        @apiHeader {String} Authorization json web token
        @apiParam {String} project Project name.
        @apiParam {Bool} ssp Is ssp.
        @apiParam {File} eggs egg file.
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 OK
        {'spider': spiders, 'number': number, 'message': 'successful'}
        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 OK
        {'message': 'failed of parameters validator'}
        """
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
        token = self.request.headers.get('Authorization')
        username = get_username(token)
        project = arguments.project.data
        ssp = arguments.ssp.data
        spiders = project
        number = 1
        eggs = self.request.files.get('eggs')
        version = str(round(time()))
        if not all([eggs, project, version]):
            return await self.interrupt(400, 'missing parameters')
        egg = eggs.pop()
        filename = egg['filename']
        if not filename.endswith('.egg'):
            return await self.interrupt(400, 'file is not egg')
        filename = await self.storage.put(egg['body'], project, version)
        if not ssp:
            gross = await get_spider_list(project, version)
            spiders = ','.join(gross)
            number = len(gross)
        await Projects.create(project=project, spiders=spiders, version=version,
                              ssp=ssp, number=number, filename=filename, creator=username,
                              create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        await self.over(201, {'spider': spiders, 'number': number, 'message': 'successful'})

    async def delete(self, *args, **kwargs):
        """
        @apiGroup Projects-delete
        @apiPermission Developer
        @api {delete} /projects/
        @apiHeader {String} Authorization json web token
        @apiParam {Int} id project id of databases.
        @apiParam {String} project Project name.
        @apiParam {Int} version project version.
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 OK
        {'project': project, 'version': version, 'message': 'successful'}
        @apiUse ErrorExamples
        """
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
        pid = arguments.id.data
        project = arguments.project.data
        version = arguments.version.data
        query = await Projects.filter(Q(id=pid) & Q(project=project) & Q(version=version))
        if query:
            try:
                await Projects.filter(id=pid).delete()
                result = self.storage.delete(self.storage.makepath(project, version))
                if result:
                    return await self.over(200, {'project': project, 'version': version, 'message': 'successful'})
            except Exception as error:
                logging.warning(error)
        await self.over(400, {'project': project, 'version': version, 'message': 'failed'})


class SchedulersHandler(RestfulHandler):
    permission = 'developer'

    async def get(self, *args, **kwargs):
        """
        @apiGroup Schedulers-get
        @apiPermission Developer
        @api {get} /Schedulers/
        @apiHeader {String} Authorization json web token
        @apiUse Operations
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {'id': 1, 'jid': 'p3fd0909803032nm', 'project': 'arts', 'spider': 'fact',
             'version': 1563206963652, 'ssp': 1, 'job': 25fd-09098f-2032-dfs20,
             'mode': 'date, 'timer': {'run_date': '2019-03-10'}, 'status': 1,
             'creator': 'username', 'create': 2019-02-22 10:00:00}
        """
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
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
        await self.over(data=response)

    async def post(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
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
            return await self.interrupt(400, 'error of timer')
        if not isinstance(timer, dict):
            return await self.interrupt(400, 'error of timer')
        status = arguments.status.data
        jid = str(uuid1())  # scheduler job id, can remove job

        if status:
            schedulers.add_job(execute_task, mode, trigger_args=timer, id=jid,
                               args=[project, spider, version, ssp, mode,
                                     arguments.timer.data, username, status])
        await Schedulers.create(project=project, spider=spider, version=version,
                                ssp=ssp, mode=mode, timer=arguments.timer.data,
                                creator=username, status=status, jid=jid,
                                create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        await self.over(201, {'project': project, 'version': version, 'status': status, 'message': 'successful'})

    async def put(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
        token = self.request.headers.get('Authorization')
        sid = arguments.id.data
        mode = arguments.mode.data
        username = get_username(token)
        status = arguments.status.data
        try:
            timer = ast.literal_eval(arguments.timer.data)
        except Exception as error:
            logging.warning(error)
            return await self.interrupt(400, 'error of timer')
        query = await Schedulers.filter(id=sid).first()
        if not query:
            return await self.interrupt(400, 'This scheduler dose not exist')
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
            return await self.interrupt(reason='No job by the id of {jid} was found.'
                                  'This may be because the timer has expired, not a fatal error.'
                                  'The corresponding scheduler will be delete.'
                                  'Don\'t worry.'.format(jid=query.jid))
        await self.over(data={'project': query.project, 'version': query.version, 'status': status, 'message': 'successful'})

    async def delete(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
        sid = arguments.id.data
        query = await Schedulers.filter(id=sid).first()
        if not query:
            return await self.interrupt(400, 'This scheduler dose not exist')
        try:
            schedulers.remove_job(query.jid)
        except JobLookupError as error:
            logging.warning(error)
        await Schedulers.filter(id=sid).delete()
        response = {'id': query.id, 'project': query.project, 'spider': query.spider,
                    'version': query.version, 'jid': query.jid, 'mode': query.mode,
                    'timer': query.timer, 'message': 'successful'}
        await self.over(200, response)


class RecordsHandler(RestfulHandler):
    async def get(self, *args, **kwargs):
        arguments = RecordsForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
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
        await self.over(data=response)


class OperationLogHandler(RestfulHandler):
    async def get(self, *args, **kwargs):
        arguments = OperationLogForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
        params, offset, limit, ordering = prep(arguments)
        query = await OperationLog.filter(**params).offset(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['results'] = [
            {'id': i.id, 'operator': i.operator, 'interface': i.interface,
             'method': i.method, 'status_code': i.status_code, 'hostname': i.hostname,
             'args': i.args, 'address': i.address, 'create': i.operation_time.strftime('%Y-%m-%d %H:%M:%S')}
            for i in query]
        await self.over(data=response)


class RegisterHandler(RestfulHandler):

    async def post(self):
        arguments = UserForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
        username = arguments.username.data
        email = arguments.email.data
        role = arguments.role.data
        password = arguments.password.data
        pwd = str_to_hash(password)
        code = random_characters(n=6)
        if role == 'superuser':
            superuser_exits = await User.filter(role='superuser').count()
            if superuser_exits:
                return await self.interrupt(400, 'superuser is exist')
        res = await User.filter(Q(username=username) | Q(email=email))
        if res:
            return await self.interrupt(400, 'username or email is exist')
        await User.create(username=username, password=pwd, email=email, code=code, role=role)
        await self.over(201, {'message': 'welcome：{username} '.format(username=username)})


class LoginHandler(RestfulHandler):
    async def post(self, *args, **kwargs):
        arguments = LoginForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
        username = arguments.username.data
        pwd = str_to_hash(arguments.password.data)
        code = arguments.code.data
        user = await User.filter(Q(username=username) & Q(password=pwd)).first()
        if not user:
            return await self.interrupt(400, 'username or password error')
        payload = {'id': user.id, 'username': user.username, 'exp': datetime.utcnow()}
        token = jwt.encode(payload, SECRET, ALGORITHM).decode('utf8')
        if user.role == 'superuser' or user.verify and user.status:
            return await self.over(data={'id': user.id, 'username': user.username, 'token': token})
        superuser = await User.filter(role='superuser').first()
        if user.status and not user.verify:
            res = await User.filter(Q(username=username) & Q(password=pwd) & Q(code=code)).first()
            if res:
                await User.filter(Q(username=username) & Q(password=pwd) & Q(code=code)).update(verify=True)
                return await self.over(data={'id': user.id, 'username': user.username, 'token': token})
            else:
                return await self.interrupt(400,
                                      'verify code error, '
                                      'please contact the superuser:{username}(email:{email})'
                                      .format(username=superuser.username, email=superuser.email))
        return await self.interrupt(400,
                              'user status is false,'
                              'please contact the superuser:{username}(email:{email})'
                              .format(username=superuser.username, email=superuser.email))


class UserHandler(RestfulHandler):

    async def get(self):
        arguments = UserForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
        params, offset, limit, ordering = prep(arguments)
        query = await User.filter(**params).offset(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['results'] = [
            {'id': i.id, 'username': i.username, 'status': i.status,
             'verify': i.verify, 'code': i.code, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
            for i in query]
        await self.over(data=response)

    async def put(self, *args, **kwargs):
        arguments = LoginForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
        uid = arguments.id.data
        password = str_to_hash(arguments.password.data) if len(arguments.password.data) > 5 else None
        status = arguments.status.data
        email = arguments.email.data
        query = await User.filter(id=uid).first()
        if not query:
            return await self.interrupt(400, 'user dose not exist')
        params = {}
        if all([email, len(email) > 5, email != query.email]):
            params['email'] = email
        if password != query.password and password:
            params['password'] = password
        if all([status, isinstance(status, bool), status != query.status]):
            params['status'] = status
        await User.filter(id=uid).update(**params)
        await self.over(data={'message': 'successful'})

    async def delete(self, *args, **kwargs):
        arguments = LoginForm(self.request.arguments)
        if not arguments.validate():
            return await self.interrupt(400, 'failed of parameters validator')
        user_id = arguments.id.data
        query = await User.filter(id=user_id).first()
        if not query:
            return await self.interrupt(400, 'user dose not exist')
        await User.filter(id=user_id).delete()
        await self.over(200, {'message': 'successful'})


