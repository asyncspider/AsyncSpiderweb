import asyncio
from test2 import pri
# async def run(cmd):
#     proc = await asyncio.create_subprocess_shell(
#         cmd,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE)
#
#     stdout, stderr = await proc.communicate()
#
#     print(f'[{cmd!r} exited with {proc.returncode}]')
#     if stdout:
#         print(f'[stdout]\n{stdout.decode()}')
#     if stderr:
#         print(f'[stderr]\n{stderr.decode()}')


async def run_pri():
    proc = await asyncio.create_subprocess_exec(pri(),
                                                   stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

asyncio.run(run_pri())
# asyncio.run(run('python -m test2.py'))