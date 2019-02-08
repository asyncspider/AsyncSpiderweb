
from tornado.web import URLSpec
from component.home.handler import IndexHandler, IncreaseHandler, JobStoreHandler
from component.admin.handler import SuperUserRegHandler, CreateUserHandler

router = [
    URLSpec('/api/v1/?', IndexHandler, name='index'),
    URLSpec('/api/v1/increase/?', IncreaseHandler, name='increase'),
    URLSpec('/api/v1/job/?', JobStoreHandler, name='job'),

    URLSpec('/api/v1/admin/reg/?', CreateUserHandler, name='reg'),
    URLSpec('/api/v1/admin/regs/?', SuperUserRegHandler, name='regs'),
]