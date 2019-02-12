import re
from wtforms_tornado import Form
from wtforms.fields import *
from wtforms.validators import *

from settings import default_page


class UserForm(Form):
    id = IntegerField()
    username = StringField()
    password = StringField()
    status = BooleanField()
    email = StringField()
    role = StringField('user role',
                       validators=[AnyOf(values=('observer', 'developer', 'superuser'),
                                         message='user role error')])
    limit = IntegerField('limit', default=default_page,
                         validators=[NumberRange(min=1, max=100,
                                                 message='limit 1-100')])
    order = StringField('order', default='id',
                        validators=[AnyOf(values=["id", "-id", "status",
                                                  "-status", "create_time", "-create_time"],
                                          message='order value not')])
    filter = StringField('filter', '', )


class LoginForm(Form):
    id = IntegerField()
    username = StringField()
    password = StringField()
    status = StringField()
    code = StringField('verify code')


class RoleForm(Form):
    id = IntegerField()
    name = StringField()
    permissions = StringField()
