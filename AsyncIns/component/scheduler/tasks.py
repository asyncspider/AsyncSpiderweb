import os
from uuid import uuid1
from datetime import datetime
import aiofiles
from ..common.util import ins_subprocess
from model import Records
from settings import spider_log_path


async def execute_task(*args, **kwargs):
    project, spider, version, ins, mode, timer, username, status = args
    job = str(uuid1())
    start, end, period, std = await ins_subprocess('component.common.runner', 'crawl',
                                                   spider, project, version, job)
    spider_log = os.path.join(spider_log_path, '{job}.log'.format(job=job))
    async with aiofiles.open(spider_log, 'w') as f:
        await f.write(std)
    await Records.create(project=project, spider=spider, version=version,
                         ins=ins, mode=mode, timer=timer,
                         creator=username, status=status, job=job,
                         start=start, end=end, period=period,
                         create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
