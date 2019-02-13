import os
from ..common.util import ins_subprocess


async def execute_task(*arg, **kwargs):
    mode = arg
    project, spider, version, ins, timer, creator, status, job = kwargs
    env = os.environ
    env['SCRAPY_PROJECT'], env['SCRAPY_VERSION'] = project, str(version)
    execute_result = await ins_subprocess(target='component.common.runner', operation='crawl', spider=spider)
    print(execute_result)
