import asyncio
import sys
import os
import datetime


class DateProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future):
        self.exit_future = exit_future
        self.output = bytearray()

    def connection_made(self, transport):
        print('start time: %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def pipe_data_received(self, fd, data):
        self.output.extend(data)

    def process_exited(self):
        print('end time: %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.exit_future.set_result(True)


async def get_date():
    loop = asyncio.get_running_loop()
    code = 'test2'
    exit_future = asyncio.Future(loop=loop)

    dp = lambda: DateProtocol(exit_future)
    transport, protocol = await loop.subprocess_exec(
        dp, sys.executable, '-m', code, 'crawl', 'baidu',
        stdin=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE)

    await exit_future
    transport.close()
    data = bytes(protocol.output)
    return data.decode('ascii').rstrip()

date = asyncio.run(get_date())
print(date)