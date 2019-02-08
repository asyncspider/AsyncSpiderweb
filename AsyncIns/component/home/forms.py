import re
from wtforms_tornado import Form
from wtforms.fields import *
from wtforms.validators import *

from settings import default_page

class IncreaseForm(Form):
    id = IntegerField('id', validators=[Regexp(regex=re.compile(('\d+')))])
    project = StringField("project name", validators=[Length(max=60,message="project name is too long")])
    version = StringField("version", validators=[Length(max=13, message='version is too long')])
    spiders = StringField("spider name list", validators=[Length(max=60,message="spider name is too long")])
    custom = BooleanField("is it scrapy") #validators=[AnyOf(values=["scrapy", "notscrapy"])]
    limit = IntegerField('limit', default=default_page, validators=[NumberRange(min=1, max=100, message='limit 1-100')])
    order = StringField('order', default='id',
                        validators=[AnyOf(values=["id", "-id", "spider_num",
                                                 "-spider_num", "create_time", "-create_time"],
                                          message='order value not')])
    filters = StringField('filter', '', )

class JobStoreForm(Form):
    project = StringField("project name", validators=[Length(max=160, message="Field Length Cannot Pass Validation")])
    version = IntegerField("version")
    spider = StringField("spider name")
    custom = BooleanField('project type')
    mode = StringField()
    timer = StringField()
    status = BooleanField('status')



class TaskQueueForm(Form):
    project = StringField("project name", validators=[Length(max=160, message="Field Length Cannot Pass Validation")])
    version = StringField("version", validators=[Length(max=32, message='version is too long')])
    spider = StringField("spider name list")
    custom = BooleanField('project type')
    sett = StringField('settings', validators=[Length(max=255, message='Field Length Cannot Pass Validation')])


