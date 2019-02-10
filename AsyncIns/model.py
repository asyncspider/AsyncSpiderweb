from tortoise.models import Model
from tortoise.fields import *


class Increase(Model):
    """ 部署 """
    id = IntField(pk=True)
    project = CharField(max_length=160,  comments="project name")
    version = CharField(max_length=64, null=True, comments="egg version")
    spiders = TextField(null=True, comments="spider list")
    custom = BooleanField(comments='True is not scrapy, False is scrapy')
    spider_num = IntField(max_length=3, null=True, verbose_name="spider number")
    egg_path = TextField(null=True, verbose_name="egg path")
    create_time = DatetimeField(auto_now=True)

    def __str__(self):
        return self.project


class RunRecord(Model):
    """ 运行记录 """
    id = IntField(pk=True)
    project = CharField(max_length=160, null=True, verbose_name="项目名称")
    spider = CharField(max_length=160, null=True, verbose_name="爬虫名称")
    version = CharField(max_length=64, null=True, verbose_name="版本号")
    job = CharField(max_length=255, null=True, verbose_name="job hash")
    pid = IntField(verbose_name="协程ID")
    log = TextField(null=True, verbose_name="日志")
    start_time = CharField(max_length=255, null=True, verbose_name="启动时间")
    end_time = CharField(max_length=255, null=True, verbose_name="结束时间")
    run_time = CharField(max_length=255, null=True, verbose_name="运行时间")


    def __str__(self):
        return self.spider


class TaskQueue(Model):
    """ 调度模型 """
    id = IntField(pk=True)
    project = CharField(max_length=160, null=True, verbose_name="项目名称")
    spider = CharField(max_length=255, null=True, verbose_name="爬虫名称")
    version = CharField(max_length=64, null=True, verbose_name="版本号")
    job_id = CharField(max_length=255, null=True, verbose_name="job hash")
    custom = BooleanField(null=True, verbose_name="是否为自定义 egg")
    sett = CharField(max_length=255, null=True, verbose_name="settings")
    create_time = DatetimeField(auto_now=True)

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
    create_time = DatetimeField(auto_now=True)

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
    role = ManyToManyField('models.Role', related_name='roles')
    create_time = DatetimeField(auto_now=True)

    def __str__(self):
        return self.username

class SuperUser(Model):
    id = IntField(pk=True)
    username = CharField(max_length=64)
    password = CharField(max_length=64)
    email = CharField(max_length=100, null=True)
    superuser = BooleanField(default=True)
    verify = BooleanField(default=False)
    create_time = DatetimeField(auto_now=True)


class Verify(Model):
    id = IntField(pk=True)
    email = CharField(max_length=100)
    code = CharField(max_length=6)
    create_time = DatetimeField(auto_now=True)

    def __str__(self):
        return self.code


class Permission(Model):
    id = IntField(pk=True)
    name = CharField(max_length=160)

    def __str__(self):
        return self.name


class Role(Model):
    id = IntField(pk=True)
    name = CharField(max_length=160)
    permissions = ManyToManyField('models.Permission', related_name='perm')
    create_time = DatetimeField(auto_now=True)

    def __str__(self):
        return self.name

#
# class GrantAuth(Model):
#     id = IntField(pk=True)
#     user = ForeignKeyField('User',  on_delete="CASCADE")
#     roles = ManyToManyField('Role')
#     create_time = DatetimeField(auto_now=True)
#
#     def __str__(self):
#         return self.user

#
# class ContentType(Model):
#     name = CharField(max_length=160)
#     model = CharField(max_length=160, comment='python model name')
#     create_time = DatetimeField(auto_now=True)
#
#
#     def __str__(self):
#         return self.name




