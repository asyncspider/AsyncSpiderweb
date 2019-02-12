from tornado.web import URLSpec
from component.home.handler import IndexHandler, DeployHandler, SchedulerHandler
from component.admin.handler import LoginHandler, RegisterHandler

router = [
    URLSpec('/api/v1/?', IndexHandler, name='index'),
    URLSpec('/api/v1/deploy/?', DeployHandler, name='deploy'),
    URLSpec('/api/v1/scheduler/?', SchedulerHandler, name='scheduler'),
    URLSpec('/api/v1/reg/?', RegisterHandler, name='reg'),
    URLSpec('/api/v1/login/?', LoginHandler, name='login'),
]
