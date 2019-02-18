import os
from datetime import datetime
from uuid import uuid1

import aiofiles
from ..parts import async_subprocess
from model import Records
from settings import SPIDER_LOG_DIR, EXECUTOR_PILOT


async def execute_task(*args, **kwargs):
    project, spider, version, ssp, mode, timer, username, status = args
    job = str(uuid1())
    start, end, period, std = await async_subprocess(EXECUTOR_PILOT, 'crawl',
                                                     spider, project, version, job)
    logfile = os.path.join(SPIDER_LOG_DIR, '{project}_{spider}_{job}.log'
                           .format(project=project, spider=spider, job=job))
    async with aiofiles.open(logfile, 'w') as f:
        await f.write(std)
    await Records.create(project=project, spider=spider, version=version,
                         ssp=ssp, mode=mode, timer=timer,
                         creator=username, status=status, job=job,
                         start=start, end=end, period=period,
                         create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
