from tornado.web import URLSpec

from component.handlers import IndexHandler, ProjectsHandler, SchedulersHandler, RecordsHandler, \
    LoginHandler, RegisterHandler, UserHandler


router = [
    URLSpec('/api/v1/?', IndexHandler, name='index'),
    URLSpec('/api/v1/user/?', UserHandler, name='user'),
    URLSpec('/api/v1/reg/?', RegisterHandler, name='reg'),
    URLSpec('/api/v1/login/?', LoginHandler, name='login'),
    URLSpec('/api/v1/records/?', RecordsHandler, name='records'),
    URLSpec('/api/v1/projects/?', ProjectsHandler, name='projects'),
    URLSpec('/api/v1/schedulers/?', SchedulersHandler, name='schedulers'),
]
