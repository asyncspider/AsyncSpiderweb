from datetime import datetime
from model import TaskQueue
import time


async def traversal_queue():
    time.sleep(5)
    print('-project-')


async def task(project, spider, version):
    print(project, spider, version, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))