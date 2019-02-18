from tortoise.models import Model
from tortoise.fields import *


class Projects(Model):
    """ project model """
    id = IntField(pk=True)
    project = CharField(max_length=100,  comments="project name")
    version = CharField(max_length=13, null=True, comments="egg version")
    spiders = TextField(null=True, comments="multiple or single spider name")
    ssp = BooleanField(comments='Is it a single spider project')
    number = IntField(max_length=3, null=True, comments="spider number")
    filename = CharField(max_length=160, null=True, comments="egg name")
    creator = CharField(max_length=64, comments='username', null=True)
    create_time = DatetimeField(null=True)

    def __str__(self):
        return self.project


class Schedulers(Model):
    """ scheduler model """
    id = IntField(pk=True)
    jid = CharField(max_length=64, comments='scheduler job id')
    project = CharField(max_length=160, null=True, comments="project name")
    spider = CharField(max_length=160, null=True, comments="spider name")
    version = CharField(max_length=64, null=True, comments="egg version")
    ssp = BooleanField(comments='Is it a single spider project')
    job = CharField(max_length=255, null=True, comments="job hash")
    mode = CharField(max_length=255, comments='timer mode,o is interval,1 is cron, 2 is date', null=True)
    timer = CharField(max_length=255, comments='time rule or time value')
    status = BooleanField(null=True, comments='scheduler status')
    creator = CharField(max_length=64, comments='creator username', null=True)
    create_time = DatetimeField(null=True)

    def __str__(self):
        return self.spider


class Records(Model):
    """ run record model """
    id = IntField(pk=True)
    project = CharField(max_length=160, null=True, comments="project name")
    spider = CharField(max_length=160, null=True, comments="spider name")
    version = CharField(max_length=64, null=True, comments="egg version")
    ssp = BooleanField(comments='Is it a single spider project')
    job = CharField(max_length=255, null=True, comments="job hash")
    mode = CharField(max_length=255, comments='timer mode,o is interval,1 is cron, 2 is date', null=True)
    timer = CharField(max_length=255, comments='time rule or time value')
    status = BooleanField(null=True, comments='scheduler status')
    start = CharField(max_length=255, null=True, comments="start time")
    end = CharField(max_length=255, null=True, comments="end time")
    period = CharField(max_length=255, null=True, comments="run time")
    creator = CharField(max_length=64, comments='creator username', null=True)
    create_time = DatetimeField(null=True)

    def __str__(self):
        return self.spider


class User(Model):
    """ user model """
    id = IntField(pk=True)
    username = CharField(max_length=64)
    password = CharField(max_length=64)
    email = CharField(max_length=100, null=True)
    status = BooleanField(default=True)
    verify = BooleanField(default=False)
    code = CharField(max_length=6)
    role = CharField(max_length=10)
    create_time = DatetimeField(null=True)

    def __str__(self):
        return self.username


class Verify(Model):
    """ verify code model """
    id = IntField(pk=True)
    email = CharField(max_length=100)
    code = CharField(max_length=6)
    create_time = DatetimeField(null=True)

    def __str__(self):
        return self.code


class OperationLog(Model):
    id = IntField(pk=True)
    operator = CharField(max_length=64, null=True)
    interface = CharField(max_length=255, null=True)
    method = CharField(max_length=64, null=True)
    status_code = IntField(null=True)
    args = TextField(null=True)
    hostname = CharField(max_length=255, null=True)
    address = CharField(max_length=64, null=True)
    operation_time = DatetimeField(null=True)



