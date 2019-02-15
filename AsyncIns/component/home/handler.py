from time import time
import ast
from tornado.web import RequestHandler

from .forms import ProjectsForm, SchedulersForm
from .storage import FileStorage
from ..common.util import *
from settings import schedulers
from component.scheduler.tasks import execute_task
from model import Projects, Schedulers, Records
from ..common.handler import RestfulHandler


class IndexHandler(RestfulHandler):
    permission = 'observer'

    # @authorization
    # async def get(self, *args, **kwargs):
    #     sec = int(self.request.arguments.get('sec')[0])
    #     schedulers.add_job(traversal_queue, 'interval', seconds=sec, max_instances=10)

    async def get(self, *args, **kwargs):
        print('this is index handler')
        data = await get_spiders('arts', '1550036771')
        logging.warning(data)


class ProjectsHandler(RestfulHandler):

    storage = FileStorage()

    async def get(self, *args, **kwargs):
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        params, offset, limit, ordering = prep(arguments)
        query = await Projects.filter(**params).offset(offset).limit(limit).order_by(ordering)
        response = dict(count=len(query))
        response['data'] = [{'id': i.id, 'project': i.project, 'spiders': i.spiders,
                            'version': i.version, 'custom': i.custom, 'spider_num': i.spider_num,
                            'egg': i.egg_path, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
                            for i in query]
        self.finish(response)

    async def post(self, *args, **kwargs):
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            return self.interrupt(400, 'failure of params validator')
        token = self.request.headers.get('Authorization')
        username = get_user_from_jwt(token) if token else None
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
            gross = await get_spiders(project, version)
            spiders = ','.join(gross)
            number = len(gross)
        await Projects.create(project=project, spiders=spiders, version=version,
                              ins=ins, number=number, filename=filename,
                              creator=username,
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
        response['data'] = [{'id': i.id, 'project': i.project, 'spider': i.spider,
                            'version': i.version, 'ins': i.ins, 'job': i.job,
                            'mode': i.mode, 'timer': i.timer, 'status': i.status,
                            'creator': i.creator,
                            'create_time': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
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
        username = get_user_from_jwt(token) if token else None
        # {'seconds': 5} {'run_date': '2019-02-13 17:05:05'}
        # {'day_of_week': 'mon-fri', 'hour': 5, 'minute': 30, 'end_date': '2014-05-30'}
        timer = ast.literal_eval(arguments.timer.data)
        status = arguments.status.data
        jid = str(uuid1())  # scheduler job id,can remove job
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
        username = get_user_from_jwt(token) if token else None
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
            schedulers.add_job(execute_task, mode, trigger_args=timer, id=query.jid,
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
        response['data'] = [{'id': i.id, 'project': i.project, 'spider': i.spider,
                            'version': i.version, 'ins': i.ins, 'job': i.job,
                            'mode': i.mode, 'timer': i.timer, 'status': i.status,
                            'start': i.start, 'end': i.end, 'period': i.period,
                            'creator': i.creator,
                            'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
                             for i in query]
        self.finish(response)


