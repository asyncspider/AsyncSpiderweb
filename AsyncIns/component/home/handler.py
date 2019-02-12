from time import time
import ast
import asyncio
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.web import RequestHandler
from tornado.httpclient import HTTPError

from .forms import DeployForm, SchedulerForm

from .storage import FileStorage
from ..common.util import authorization, finish_resp, get_scrapy_spiders
from settings import schedulers
from component.scheduler.tasks import traversal_queue, task
from model import Deploy


class IndexHandler(RequestHandler):
    permission = 'observer'

    @authorization
    async def get(self, *args, **kwargs):
        sec = int(self.request.arguments.get('sec')[0])
        schedulers.add_job(traversal_queue, 'interval', seconds=sec, max_instances=10)


class DeployHandler(RequestHandler):

    def initialize(self):
        self.filestorage = FileStorage()

    async def get(self, *args, **kwargs):
        """  """
        arguments = DeployForm(self.request.arguments)
        if not arguments.validate():
            finish_resp(self, 400, 'field validators error')
            return None
        order = arguments.order.data
        limit = arguments.limit.data
        res = await arguments.filter().limit(limit).order_by(order)
        item = dict(count=len(res))
        item['data'] = [{'id': i.id, 'project': i.project, 'spiders': i.spiders,
                         'version': i.version, 'custom': i.custom, 'spider_num': i.spider_num,
                         'egg': i.egg_path, 'create': i.create_time.strftime('%Y-%m-%d %H:%M:%S')}
                        for i in res]
        self.finish(item)

    async def post(self, *args, **kwargs):
        arguments = DeployForm(self.request.arguments)
        # if not arguments.validate():
        #
        #     finish_resp(self, 400, 'field validators error')
        #     return None
        project = arguments.project.data
        spiders = arguments.spiders.data
        ins = arguments.ins.data
        eggs = self.request.files.get('eggs')
        version = round(time())
        if not all([eggs, project, version]):
            finish_resp(self, 400, 'missing parameters')
            return None
        egg = eggs.pop()
        filename = egg['filename']
        if not filename.endswith('.egg'):
            raise HTTPError(400, message='file is not egg')
        file_path = await self.filestorage.put(egg['body'], project, version)
        if ins:
            spiders = ''
            print(spiders)
        else:
            spiders = asyncio.run(get_scrapy_spiders(project, version))
            print(spiders)
        await Deploy.create(project=project, spiders=spiders,
                               ins=ins, version=version, egg_path=file_path)

    async def delete(self, *args, **kwargs):
        arguments = DeployForm(self.request.arguments)
        if not arguments.validate(): raise HTTPError(400, message='params is error')  # wtf validate
        project = arguments.project.data
        version = arguments.version.data
        await self.filestorage.delete(project, version)

    # async def put(self, *args, **kwargs):
    #     increase = IncreaseForm(self.request.arguments)
    #     if not increase.validate(): raise HTTPError(400, message='params is error')  # wtf validate
    #     id = increase.id.data
    #     project = increase.project.data
    #     version = increase.version.data


class SchedulerHandler(RequestHandler):
    async def post(self, *args, **kwargs):
        arguments = SchedulerForm(self.request.arguments)
        if not arguments.validate(): raise HTTPError(400, message='params is error')  # wtf validate
        project = arguments.project.data
        version = arguments.version.data
        spider = arguments.spider.data
        ins = arguments.ins.data
        mode = arguments.mode.data
        timer = ast.literal_eval(arguments.timer.data)
        status = arguments.status.data
        schedulers.add_job(task, mode, trigger_args=timer,
                           kwargs={"project": project, "spider": spider, "version": version}, )

        #
        # async with Environment(project, spider, version) as eir:
        #     await eir.ecs()


