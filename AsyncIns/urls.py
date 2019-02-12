
from tornado.web import URLSpec
from component.home.handler import IndexHandler, IncreaseHandler, SchedulerHandler
from component.admin.handler import LoginHandler, RegisterHandler

router = [
    URLSpec('/api/v1/?', IndexHandler, name='index'),
    URLSpec('/api/v1/increase/?', IncreaseHandler, name='increase'),
    URLSpec('/api/v1/scheduler/?', SchedulerHandler, name='scheduler'),
    URLSpec('/api/v1/reg/?', RegisterHandler, name='reg'),
    URLSpec('/api/v1/login/?', LoginHandler, name='login'),
]
#
# for i in router:
#     dps = i.name
#     print(i.handler_class)