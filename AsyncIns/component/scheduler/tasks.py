from datetime import datetime
from model import TaskQueue


async def traversal_queue():
    traversals = await TaskQueue.all()
    for traversal in traversals:
        project = traversal.project
        spider = traversal.spider
        print(project, spider)