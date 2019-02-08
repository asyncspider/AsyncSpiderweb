import uuid
import os
import json
from time import time
from tornado.web import RequestHandler
from tornado.httpclient import HTTPError
from tortoise.queryset import Q
import aiofiles
from model import Increase, TaskQueue, User
from .forms import IncreaseForm, TaskQueueForm, JobStoreForm
from settings import settings, schedulers
from .storage import FileStorage
from .executor import Environment
from concurrent.futures import ProcessPoolExecutor


class IndexHandler(RequestHandler):
    async def get(self, *args, **kwargs):
        self.write('Octopus is running')



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


#
# class TaskQueueHandler(RequestHandler):
#
#
#     async def tra(self):
#         print(5)
#
#     async def get(self, *args, **kwargs):
#
#         schedulers.add_job(self.tra, 'interval', seconds=9)
#         param = [self.tra, 'interval', 9]
#
#
#
#     async def post(self, *args, **kwargs):
#         task = TaskQueueForm(self.request.arguments)
#         if task.validate():
#             project = task.project.data
#             spider = task.spider.data
#             version = task.version.data
#             custom = task.custom.data
#             sett = task.sett.data
#             job_id = str(uuid.uuid4())
#             await TaskQueue.create(project=project, spider=spider, version=version,
#                                    custom=custom, sett=sett, job_id=job_id)


class JobStoreHandler(RequestHandler):
    async def post(self, *args, **kwargs):
        job = JobStoreForm(self.request.arguments)
        if not job.validate(): raise HTTPError(400, message='params is error')  # wtf validate
        project = job.project.data
        version = job.version.data
        spider = job.spider.data
        custom = job.custom.data
        mode = job.mode.data
        timer = job.timer.data
        status = job.status.data
        async with Environment(project, version) as eir:
            await eir.ecs()

