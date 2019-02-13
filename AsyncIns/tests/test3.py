import asyncio
import sys
import os
from asyncio.subprocess import PIPE


async def executors():
    env = os.environ.copy()
    proc = await asyncio.create_subprocess_shell(sys.executable, '-m test',
                                                 stdout=PIPE, stderr=PIPE, stdin=PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

asyncio.run(executors())

