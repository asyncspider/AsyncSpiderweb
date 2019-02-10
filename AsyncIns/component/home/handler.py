import uuid
import os

from time import time
import ast
from tornado.web import RequestHandler
from tornado.httpclient import HTTPError

from model import Increase
from .forms import IncreaseForm, SchedulerForm

from .storage import FileStorage
from .executor import Environment
from concurrent.futures import ProcessPoolExecutor
from ..common.util import authorization
from settings import schedulers
from component.scheduler.tasks import traversal_queue, task


class IndexHandler(RequestHandler):
    @authorization
    async def post(self, *args, **kwargs):
        sec = int(self.request.arguments.get('sec')[0])
        schedulers.add_job(traversal_queue, 'interval', seconds=sec, max_instances=10)


class IncreaseHandler(RequestHandler):

    def initialize(self):
        self.filestorage = FileStorage()

    async def get(self, *args, **kwargs):
        """
        order/limit
        """
        increase = IncreaseForm(self.request.arguments)
        if increase.validate():
            order = increase.order.data
            limit = increase.limit.data
        res = await Increase.filter().limit(limit).order_by(order)
        item = {}
        item['count'] = len(res)
        item['data'] = [{'id': i.id, 'project': i.project, 'spiders': i.spiders,
                         'version': i.version, 'custom': i.custom, 'spider_num': i.spider_num,
                         'egg': i.egg_path, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
                         for i in res]
        self.finish(item)

    async def post(self, *args, **kwargs):
        increase = IncreaseForm(self.request.arguments)
        if not increase.validate(): raise HTTPError(400, message='params is error') # wtf validate
        project = increase.project.data
        spiders = increase.spiders.data
        custom = increase.custom.data
        eggs = self.request.files.get('eggs')
        version = round(time()) # current timestamp is version number
        if not all([eggs, project, version]): raise HTTPError(400, message='missing parameters')
        egg = eggs.pop()
        filename = egg['filename']
        if not filename.endswith('.egg'): raise HTTPError(400, message='file is not egg')
        file_path = await self.filestorage.put(egg['body'], project, version)
        await Increase.create(project=project, spiders=spiders,
                              custom=custom, version=version,egg_path=file_path)

    async def delete(self, *args, **kwargs):
        increase = IncreaseForm(self.request.arguments)
        if not increase.validate(): raise HTTPError(400, message='params is error')  # wtf validate
        project = increase.project.data
        version = increase.version.data
        await self.filestorage.delete(project, version)

    # async def put(self, *args, **kwargs):
    #     increase = IncreaseForm(self.request.arguments)
    #     if not increase.validate(): raise HTTPError(400, message='params is error')  # wtf validate
    #     id = increase.id.data
    #     project = increase.project.data
    #     version = increase.version.data


class SchedulerHandler(RequestHandler):
    async def post(self, *args, **kwargs):
        job = SchedulerForm(self.request.arguments)
        if not job.validate(): raise HTTPError(400, message='params is error')  # wtf validate
        project = job.project.data
        version = job.version.data
        spider = job.spider.data
        ins = job.ins.data
        mode = job.mode.data
        timer = ast.literal_eval(job.timer.data)
        status = job.status.data
        schedulers.add_job(task, mode, trigger_args=timer, kwargs={"project": project, "spider": spider, "version": version}, )

        #
        # async with Environment(project, spider, version) as eir:
        #     await eir.ecs()


