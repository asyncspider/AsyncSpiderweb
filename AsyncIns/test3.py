from tornado.process import Subprocess
from tornado.ioloop import IOLoop
import logging

async def run_pri():
    proc = Subprocess('ls',
                                                   stdout=Subprocess.STREAM,
                                                   stderr=Subprocess.STREAM)

    stdout = proc.stdout.reading()
    stderr = proc.stderr
    stdin = proc.stdin
    pid = proc.pid
    stdout.write()


if __name__ == "__main__":
    loop = IOLoop.current()
    loop.run_sync(run_pri)