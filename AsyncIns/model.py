import datetime
from tortoise.models import Model
from tortoise.fields import *


class Projects(Model):
    """ 项目模型 """
    id = IntField(pk=True)
    project = CharField(max_length=100,  comments="project name")
    version = CharField(max_length=13, null=True, comments="egg version")
    spiders = TextField(null=True, comments="spider list")
    ins = BooleanField(comments='asyncins or scrapy. True is asyncins')
    number = IntField(max_length=3, null=True, comments="spider number")
    filename = CharField(max_length=160, null=True, comments="egg name")
    creator = CharField(max_length=64, comments='creator username', null=True)
    create_time = DatetimeField(null=True)

    def __str__(self):
        return self.project


class SchedulerRecord(Model):
    """ 运行记录模型 """
    id = IntField(pk=True)
    project = CharField(max_length=160, null=True, comments="project name")
    spider = CharField(max_length=160, null=True, comments="spider name")
    version = CharField(max_length=64, null=True, comments="egg version")
    job = CharField(max_length=255, null=True, comments="job hash")
    pid = IntField(verbose_name="process id", null=True)
    start_time = CharField(max_length=255, null=True, comments="start time")
    end_time = CharField(max_length=255, null=True, comments="end time")
    run_time = CharField(max_length=255, null=True, comments="run time")
    create_time = DatetimeField(null=True)

    def __str__(self):
        return self.spider


class JobStore(Model):
    """ name of task/mode of task/function name/time rule/is it enable/ """
    id = IntField(pk=True)
    job = CharField(max_length=160, comments="job name")
    project = CharField(max_length=160, comments="project name")
    version = CharField(max_length=13, null=True, comments="egg version")
    spider = CharField(max_length=160, null=True, comments="spider name")
    mode = IntField(default=0, comments='timer mode,o is interval,1 is cron, 2 is date')
    timer = CharField(max_length=255, comments='time rule or time value')
    status = BooleanField(default=True, comments='is it enable, True is enable, False is disable')
    creator = ForeignKeyField('models.User', related_name='creator', comments='the job creator')
    create_time = DatetimeField(null=True)

    def __str__(self):
        return self.job


class User(Model):
    id = IntField(pk=True)
    username = CharField(max_length=64)
    password = CharField(max_length=64)
    email = CharField(max_length=100, null=True)
    status = BooleanField(default=True)
    verify = BooleanField(default=False)
    code = CharField(max_length=6)
    role = CharField(max_length=10)
    remark = CharField(max_length=64)
    create_time = DatetimeField(null=True)

    def __str__(self):
        return self.username


class Verify(Model):
    id = IntField(pk=True)
    email = CharField(max_length=100)
    code = CharField(max_length=6)
    create_time = DatetimeField(null=True)

    def __str__(self):
        return self.code


