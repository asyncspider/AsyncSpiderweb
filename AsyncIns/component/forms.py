import re
from wtforms_tornado import Form
from wtforms.fields import *
from wtforms.validators import *

from settings import DEFAULT_PAGE, DEFAULT_OFFSET


class ProjectsForm(Form):
    id = IntegerField('id')
    project = StringField("project name", validators=[Length(max=100, message="project name is too long")])
    version = StringField("version", validators=[Length(max=13, message='version is too long')])
    spiders = StringField("multiple or single spider name")
    ssp = BooleanField("Is it single spider project")
    offset = IntegerField('offset', default=DEFAULT_OFFSET)
    limit = IntegerField('limit', default=DEFAULT_PAGE, validators=[NumberRange(min=1, max=100, message='limit 1-100')])
    ordering = StringField('ordering', default='id',
                           validators=[AnyOf(values=["id", "-id", "number",
                                                     "-number", "create_time", "-create_time"],
                                             message='error of ordering parameters')])


class SchedulersForm(Form):
    id = IntegerField('id')
    project = StringField("project name", validators=[Length(max=100, message="project name is too long")])
    version = StringField("version")
    spider = StringField("spider name")
    ssp = BooleanField("Is it single spider project")
    mode = StringField('mode', validators=[AnyOf(values=('date', 'interval', 'cron', ''), message='mode error')])
    timer = StringField()
    status = BooleanField('status')
    offset = IntegerField('offset', default=DEFAULT_OFFSET)
    limit = IntegerField('limit', default=DEFAULT_PAGE, validators=[NumberRange(min=1, max=100, message='limit 1-100')])
    ordering = StringField('order', default='id',
                           validators=[AnyOf(values=["id", "-id", "status",
                                       "-status", "create_time", "-create_time"],
                                             message='error of ordering parameters')])


class UserForm(Form):
    id = IntegerField()
    username = StringField()
    password = StringField()
    status = BooleanField()
    email = StringField()
    role = StringField('user role',
                       validators=[AnyOf(values=('observer', 'developer', 'superuser'),
                                         message='user role error')])
    offset = IntegerField('offset', default=DEFAULT_OFFSET)
    limit = IntegerField('limit', default=DEFAULT_PAGE, validators=[NumberRange(min=1, max=100, message='limit 1-100')])
    ordering = StringField('ordering', default='id',
                           validators=[AnyOf(values=["id", "-id", "verify",
                                                     "-verify", "status",  "-status",
                                                     "create_time", "-create_time"],
                                             message='error of ordering parameters')])


class LoginForm(Form):
    id = IntegerField()
    username = StringField()
    password = StringField('password')
    email = StringField()
    status = StringField()
    code = StringField('verify code')


class RecordsForm(Form):
    id = IntegerField('id')
    project = StringField("project name", validators=[Length(max=100, message="project name is too long")])
    version = StringField("version")
    spider = StringField("spider name")
    ssp = BooleanField("Is it single spider project")
    mode = StringField('mode', validators=[AnyOf(values=('date', 'interval', 'cron', ''), message='mode error')])
    timer = StringField()
    status = BooleanField('status')
    offset = IntegerField('offset', default=DEFAULT_OFFSET)
    limit = IntegerField('limit', default=DEFAULT_PAGE, validators=[NumberRange(min=1, max=100, message='limit 1-100')])
    ordering = StringField('order', default='id',
                           validators=[AnyOf(values=["id", "-id", "status",
                                       "-status", "create_time", "-create_time"],
                                             message='error of ordering parameters')])
class OperationLogForm(Form):
    id = IntegerField('id')
    project = StringField("project name", validators=[Length(max=100, message="project name is too long")])
    version = StringField("version")
    spider = StringField("spider name")
    ssp = BooleanField("Is it single spider project")
    mode = StringField('mode', validators=[AnyOf(values=('date', 'interval', 'cron', ''), message='mode error')])
    timer = StringField()
    status = BooleanField('status')
    offset = IntegerField('offset', default=DEFAULT_OFFSET)
    limit = IntegerField('limit', default=DEFAULT_PAGE, validators=[NumberRange(min=1, max=100, message='limit 1-100')])
    ordering = StringField('order', default='id',
                           validators=[AnyOf(values=["id", "-id", "status",
                                       "-status", "create_time", "-create_time"],
                                             message='error of ordering parameters')])
