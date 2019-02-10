
from tornado.web import URLSpec
from component.home.handler import IndexHandler, IncreaseHandler, SchedulerHandler
from component.admin.handler import SuperUserRegHandler, CreateUserHandler, LoginHandler, RoleHandler

router = [
    URLSpec('/api/v1/?', IndexHandler, name='index'),
    URLSpec('/api/v1/increase/?', IncreaseHandler, name='increase'),
    URLSpec('/api/v1/scheduler/?', SchedulerHandler, name='scheduler'),

    URLSpec('/api/v1/admin/reg/?', CreateUserHandler, name='reg'),
    URLSpec('/api/v1/admin/regs/?', SuperUserRegHandler, name='regs'),
    URLSpec('/api/v1/admin/login/?', LoginHandler, name='login'),
    URLSpec('/api/v1/admin/role/?', RoleHandler, name='role'),
]
#
# for i in router:
#     dps = i.name
#     print(i.handler_class)