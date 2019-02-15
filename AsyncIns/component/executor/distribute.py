import os
from datetime import datetime
from uuid import uuid1

import aiofiles
from ..parts import async_subprocess
from model import Records
from settings import SPIDER_LOG_DIR


async def execute_task(*args, **kwargs):
    project, spider, version, ins, mode, timer, username, status = args
    job = str(uuid1())
    start, end, period, std = await async_subprocess('executor.pilot', 'crawl',
                                                     spider, project, version, job)
    spider_log = os.path.join(SPIDER_LOG_DIR, '{job}.log'.format(job=job))
    async with aiofiles.open(spider_log, 'w') as f:
        await f.write(std)
    await Records.create(project=project, spider=spider, version=version,
                         ins=ins, mode=mode, timer=timer,
                         creator=username, status=status, job=job,
                         start=start, end=end, period=period,
                         create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
