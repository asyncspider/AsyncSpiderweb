from time import time
from datetime import datetime
import ast
import os
import logging
from uuid import uuid1
from tornado.web import RequestHandler
from tornado.httpclient import HTTPError

from .forms import ProjectsForm, SchedulersForm

from .storage import FileStorage
from ..common.util import *
from settings import schedulers
from component.scheduler.tasks import execute_task
from model import Projects, Schedulers
from tortoise.queryset import Q


class IndexHandler(RequestHandler):
    permission = 'observer'

    # @authorization
    # async def get(self, *args, **kwargs):
    #     sec = int(self.request.arguments.get('sec')[0])
    #     schedulers.add_job(traversal_queue, 'interval', seconds=sec, max_instances=10)

    async def get(self, *args, **kwargs):
        print('this is index handler')
        # target='tests.test2'
        data = await get_spiders('arts', '1550036771')
        # data = await ins_subprocess('component.common.runner', 'list',
        #                             project='arts', spider='baidu', version='1550036771',
        #                             job=str(uuid1())
        #                             )
        logging.warning(data)


class ProjectsHandler(RequestHandler):

    def initialize(self):
        self.filestorage = FileStorage()

    async def get(self, *args, **kwargs):
        """  """
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate():
            finish_resp(self, 400, 'field validators error')
            return
        order = arguments.order.data
        limit = arguments.limit.data
        res = await Projects.filter().limit(limit).order_by(order)
        item = dict(count=len(res))
        item['data'] = [{'id': i.id, 'project': i.project, 'spiders': i.spiders,
                         'version': i.version, 'custom': i.custom, 'spider_num': i.spider_num,
                         'egg': i.egg_path, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
                        for i in res]
        self.finish(item)

    async def post(self, *args, **kwargs):
        arguments = ProjectsForm(self.request.arguments)
        token = self.request.headers.get('Authorization')
        username = get_user_from_jwt(token) if token else None
        project = arguments.project.data
        ins = arguments.ins.data
        spiders = project
        number = 1
        eggs = self.request.files.get('eggs')
        version = str(round(time()))
        if not all([eggs, project, version]):
            finish_resp(self, 400, 'missing parameters')
            return
        egg = eggs.pop()
        filename = egg['filename']
        if not filename.endswith('.egg'):
            finish_resp(self, 400, 'file is not egg')
            return
        filename = await self.filestorage.put(egg['body'], project, version)
        if not ins:
            gross = await get_spiders(project, version)
            spiders = ','.join(gross)
            number = len(gross)
        await Projects.create(project=project, spiders=spiders, version=version,
                              ins=ins, number=number, filename=filename,
                              creator=username,
                              create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        finish_resp(self, 201, {'spider': spiders, 'number': number})
        return

    async def delete(self, *args, **kwargs):
        arguments = ProjectsForm(self.request.arguments)
        if not arguments.validate(): raise HTTPError(400, message='params is error')  # wtf validate
        project = arguments.project.data
        version = arguments.version.data
        await self.filestorage.delete(project, version)
        res = await Projects.filter(Q(project=project) & Q(version=version)).first().delete()
        finish_resp(self, 204, {'project': project, 'version': version, 'delete': res})
        return


class SchedulersHandler(RequestHandler):

    async def get(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        # if not arguments.validate():
        #     finish_resp(self, 400, 'field validators error')
        #     return
        order = arguments.order.data
        limit = arguments.limit.data
        res = await Schedulers.filter().limit(limit).order_by(order)
        item = dict(count=len(res))
        item['data'] = [{'id': i.id, 'project': i.project, 'spider': i.spider,
                         'version': i.version, 'ins': i.ins, 'job': i.job,
                         'mode': i.mode, 'timer': i.timer, 'status': i.status,
                         'creator': i.creator,
                         'create_time': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
                        for i in res]
        # item['data'] = [{'id': i.id, 'project': i.project, 'spider': i.spider,
        #                  'version': i.version, 'ins': i.ins, 'job': i.job,
        #                  'mode': i.mode, 'timer': i.timer, 'status': i.status,
        #                  'start': i.start, 'end': i.end, 'period': i.period,
        #                  'creator': i.creator,
        #                  'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
        #                 for i in res]
        self.finish(item)

    async def post(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
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

    async def put(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        token = self.request.headers.get('Authorization')
        sid = arguments.id.data
        version = arguments.version.data
        mode = arguments.mode.data
        timer = ast.literal_eval(arguments.timer.data) or ''
        username = get_user_from_jwt(token) if token else None
        status = arguments.status.data
        query = await Schedulers.filter(id=sid).first()
        if query.status and not status:  # cancel task according to status
            try:
                schedulers.remove_job(query.jid)
            except Exception as error:
                logging.error(error)
        if status and not query.status:  # add task according to status
            schedulers.add_job(execute_task, mode, trigger_args=timer, id=query.jid,
                               args=[query.project, query.spider, version, mode, timer, username, status])
        await Schedulers.filter(id=sid).update(mode=mode, timer=arguments.timer.data,
                                               creator=username, status=status)


class RecordsHandler(RequestHandler):
    async def get(self, *args, **kwargs):
        arguments = SchedulersForm(self.request.arguments)
        # if not arguments.validate():
        #     finish_resp(self, 400, 'field validators error')
        #     return
        order = arguments.order.data
        limit = arguments.limit.data
        res = await Schedulers.filter().limit(limit).order_by(order)
        item = dict(count=len(res))
        item['data'] = [{'id': i.id, 'project': i.project, 'spider': i.spider,
                         'version': i.version, 'ins': i.ins, 'job': i.job,
                         'mode': i.mode, 'timer': i.timer, 'status': i.status,
                         'start': i.start, 'end': i.end, 'period': i.period,
                         'creator': i.creator,
                         'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
                        for i in res]
        self.finish(item)


