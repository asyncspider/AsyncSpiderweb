import asyncio
import sys, os
from subprocess import Popen, PIPE


async def get_date():
    code = 'import datetime; print(datetime.datetime.now())'

    # Create the subprocess; redirect the standard output
    # into a pipe.
    # proc = await asyncio.create_subprocess_exec(
    #     sys.executable, '-m', 'test2', 'list',
    #     stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'UTF-8'
    env['SCRAPY_PROJECT'] = 'arts'
    # proc = await asyncio.create_subprocess_exec(
    #     sys.executable, '-m', 'test2.py', 'crawl',
    #     stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    proc = await asyncio.create_subprocess_exec(sys.executable, '-m', 'test.py',
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    # Read one line of output.
    out, err = await proc.communicate()

    # Wait for the subprocess exit.
    await proc.wait()
    return out

# res = asyncio.run(executeors())
# date = asyncio.run(get_date())
# print(f"Current date: {date}")
if __name__ == '__main__':
    from tornado.ioloop import IOLoop
    loop = IOLoop.current()
    date = loop.run_sync(get_date)
    print(date)
