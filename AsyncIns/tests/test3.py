import asyncio
import sys
import os
from asyncio.subprocess import PIPE

async def executors():
    env = os.environ.copy()
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test2.py')
    proc = await asyncio.create_subprocess_exec(sys.executable, '-m', 'test2.py', 'list', stdout=PIPE, stderr=PIPE, env=env)

    stdout, stderr = await proc.communicate()

    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

asyncio.run(executors())

