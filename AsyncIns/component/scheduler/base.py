import six
from functools import wraps
from apscheduler.util import maybe_ref
from datetime import timedelta

from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.util import undefined
from apscheduler.job import Job
from apscheduler.schedulers.base import STATE_STOPPED

try:
    from tornado.ioloop import IOLoop
except ImportError:
    raise ImportError('TornadoScheduler requires tornado installed')


class CustomBaseScheduler(BaseScheduler):

    def add_job(self, func, trigger=None, trigger_args=None, args=None, kwargs=None, id=None, name=None,
                misfire_grace_time=undefined, coalesce=undefined, max_instances=undefined,
                next_run_time=undefined, jobstore='default', executor='default',
                replace_existing=False):

        """
        :param trigger_args: dict
        """
        job_kwargs = {
            'trigger': self._create_trigger(trigger, trigger_args),
            'executor': executor,
            'func': func,
            'args': tuple(args) if args is not None else (),
            'kwargs': dict(kwargs) if kwargs is not None else {},
            'id': id,
            'name': name,
            'misfire_grace_time': misfire_grace_time,
            'coalesce': coalesce,
            'max_instances': max_instances,
            'next_run_time': next_run_time
        }
        job_kwargs = dict((key, value) for key, value in six.iteritems(job_kwargs) if
                          value is not undefined)
        job = Job(self, **job_kwargs)

        # Don't really add jobs to job stores before the scheduler is up and running
        with self._jobstores_lock:
            if self.state == STATE_STOPPED:
                self._pending_jobs.append((job, jobstore, replace_existing))
                self._logger.info('Adding job tentatively -- it will be properly scheduled when '
                                  'the scheduler starts')
            else:
                self._real_add_job(job, jobstore, replace_existing)

        return job


def run_in_ioloop(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._ioloop.add_callback(func, self, *args, **kwargs)
    return wrapper


class TornadoScheduler(CustomBaseScheduler):
    """
    A scheduler that runs on a Tornado IOLoop.

    The default executor can run jobs based on native coroutines (``async def``).

    =========== ===============================================================
    ``io_loop`` Tornado IOLoop instance to use (defaults to the global IO loop)
    =========== ===============================================================
    """

    _ioloop = None
    _timeout = None

    @run_in_ioloop
    def shutdown(self, wait=True):
        super(TornadoScheduler, self).shutdown(wait)
        self._stop_timer()

    def _configure(self, config):
        self._ioloop = maybe_ref(config.pop('io_loop', None)) or IOLoop.current()
        super(TornadoScheduler, self)._configure(config)

    def _start_timer(self, wait_seconds):
        self._stop_timer()
        if wait_seconds is not None:
            self._timeout = self._ioloop.add_timeout(timedelta(seconds=wait_seconds), self.wakeup)

    def _stop_timer(self):
        if self._timeout:
            self._ioloop.remove_timeout(self._timeout)
            del self._timeout

    def _create_default_executor(self):
        from apscheduler.executors.tornado import TornadoExecutor
        return TornadoExecutor()

    @run_in_ioloop
    def wakeup(self):
        self._stop_timer()
        wait_seconds = self._process_jobs()
        self._start_timer(wait_seconds)
