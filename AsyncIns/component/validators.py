import re
from wtforms_tornado import Form
from wtforms.fields import *
from wtforms.validators import *

from settings import DEFAULT_PAGE, DEFAULT_OFFSET


class ProjectsForm(Form):
    id = IntegerField('id')
    project = StringField("project name", validators=[Length(max=100, message="project name is too long")])
    version = StringField("version", validators=[Length(max=13, message='version is too long')])
    spiders = StringField("spider name list", validators=[Length(max=60, message="spider name is too long")])
    ins = BooleanField("is it scrapy")
    offset = IntegerField('offset', default=DEFAULT_OFFSET)
    limit = IntegerField('limit', default=DEFAULT_PAGE, validators=[NumberRange(min=1, max=100, message='limit 1-100')])
    ordering = StringField('order', default='id',
                           validators=[AnyOf(values=["id", "-id", "number",
                                                     "-number", "create_time", "-create_time"],
                                             message='ordering params error')])


class SchedulersForm(Form):
    id = IntegerField('id', validators=[Regexp(regex=re.compile(('\d+')))])
    project = StringField("project name", validators=[Length(max=160, message="Field Length Cannot Pass Validation")])
    version = StringField("version")
    spider = StringField("spider name")
    ins = BooleanField('asyncins or scrapy. True is asyncins')
    mode = StringField('mode', validators=[AnyOf(values=('date', 'interval', 'cron'), message='mode error')])
    timer = StringField()
    status = BooleanField('status')
    offset = IntegerField('offset')
    limit = IntegerField('limit', default=DEFAULT_PAGE, validators=[NumberRange(min=1, max=100, message='limit 1-100')])
    ordering = StringField('order', default='id',
                           validators=[AnyOf(values=["id", "-id", "number",
                                       "-number", "create_time", "-create_time"],
                                             message='order value not')])


class RecordsForm(Form):
    pass


class UserForm(Form):
    id = IntegerField()
    username = StringField()
    password = StringField()
    status = BooleanField()
    email = StringField()
    # role = StringField('user role',
    #                    validators=[AnyOf(values=('observer', 'developer', 'superuser'),
    #                                      message='user role error')])
    offset = IntegerField('offset', default=999)
    limit = IntegerField('limit', default=DEFAULT_PAGE, validators=[NumberRange(min=1, max=100, message='limit 1-100')])
    ordering = StringField('order', default='id',
                           validators=[AnyOf(values=["id", "-id", "username",
                                                     "-username", "status",  "-status",
                                                     "create_time", "-create_time"],
                                             message='order value not')])


class LoginForm(Form):
    id = IntegerField()
    username = StringField()
    password = StringField('password')
    email = StringField()
    status = StringField()
    code = StringField('verify code')


class RegisterForm(Form):
    pass


class RoleForm(Form):
    id = IntegerField()
    name = StringField()
    permissions = StringField()
