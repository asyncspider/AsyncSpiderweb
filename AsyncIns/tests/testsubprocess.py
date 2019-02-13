from tornado.process import Subprocess
from tornado import ioloop
from asyncio.subprocess import PIPE
from datetime import datetime


# class Subs(Subprocess):
#     def set_exit_callback(self, callback):
#         self._exit_callback = stack_context.wrap(callback)
#         Subprocess.initialize()
#         Subprocess._waiting[self.pid] = self
#         Subprocess._try_cleanup_process(self.pid)
#


async def runner():
    p = Subprocess(['python -m test'], stdout=PIPE, stderr=PIPE, shell=True)
    out, err = await p.stdout.read(), p.stderr.read()
    p.set_exit_callback(ends(out, err))



def ends(std, out, err):
    print(std)
    print('end time:')
    print(datetime.now())

if __name__ == '__main__':
    loop = ioloop.IOLoop.current()
    loop.run_sync(runner())


