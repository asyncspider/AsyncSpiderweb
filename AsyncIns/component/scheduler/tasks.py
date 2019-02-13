import os
from uuid import uuid1
from datetime import datetime
from ..common.util import ins_subprocess
from model import Records


async def execute_task(*args, **kwargs):
    project, spider, version, ins, mode, timer, username, status = args
    job = str(uuid1())
    env = os.environ
    env['SCRAPY_PROJECT'], env['SCRAPY_VERSION'], env['SCRAPY_JOB'] = project, str(version), job
    start, end, period, std = await ins_subprocess(target='component.common.runner', operation='crawl', spider=spider)
    await Records.create(project=project, spider=spider, version=version,
                         ins=ins, mode=mode, timer=timer,
                         creator=username, status=status, job=job,
                         start=start, end=end, period=period,
                         create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
