import re
from wtforms_tornado import Form
from wtforms.fields import *
from wtforms.validators import *

from settings import default_page


class DeployForm(Form):
    id = IntegerField('id', validators=[Regexp(regex=re.compile(('\d+')))])
    project = StringField("project name", validators=[Length(max=100, message="project name is too long")])
    version = StringField("version", validators=[Length(max=13, message='version is too long')])
    spiders = StringField("spider name list", validators=[Length(max=60, message="spider name is too long")])
    ins = BooleanField("is it scrapy")
    limit = IntegerField('limit', default=default_page, validators=[NumberRange(min=1, max=100, message='limit 1-100')])
    order = StringField('order', default='id',
                        validators=[AnyOf(values=["id", "-id", "spider_num",
                                                 "-spider_num", "create_time", "-create_time"],
                                          message='order value not')])
    filters = StringField('filter', '', )


class SchedulerForm(Form):
    project = StringField("project name", validators=[Length(max=160, message="Field Length Cannot Pass Validation")])
    version = IntegerField("version")
    spider = StringField("spider name")
    ins = BooleanField('project type')
    mode = StringField('mode', validators=[AnyOf(values=('date', 'interval', 'cron'), message='mode error')])
    timer = StringField()
    status = BooleanField('status')


