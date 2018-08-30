import redis
import time
import asyncio
from investment.transaction.services import *
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from config import TaskConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


# class ScheduleFactory(object):
#     def __init__(self):
#         if not hasattr(ScheduleFactory, '__scheduler'):
#             __scheduler = ScheduleFactory.get_instance()
#         self.scheduler = __scheduler
#
#     @staticmethod
#     def get_instance():
#         pool = redis.ConnectionPool(
#             host='172.24.132.208',
#             port=6379,
#         )
#         r = redis.StrictRedis(host='127.0.0.1', port=6379)
#         jobstores = {
#             'redis': RedisJobStore(2, r),
#             'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
#         }
#         executors = {
#             'default': ThreadPoolExecutor(max_workers=30),
#             'processpool': ProcessPoolExecutor(max_workers=30)
#         }
#         job_defaults = {
#             'coalesce': False,
#             'max_instances': 3
#         }
#         scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults,
#                                         daemonic=False)
#
#         return scheduler
#
#     def start(self):
#         self.scheduler.start()
#
#     def shutdown(self):
#         self.scheduler.shutdown()


# jobstores = {
#     'mongo': MongoDBJobStore(),
#     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
# }
# executors = {
#     'default': ThreadPoolExecutor(20),
#     'processpool': ProcessPoolExecutor(5)
# }
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 3
# }
# scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
scheduler = BackgroundScheduler()

# @scheduler.scheduled_job('cron', second='*/5', id='ea_task',)
def try_trade():
    ExpertAdvisorService.start()

    print('Tick! The time is: %s' % datetime.now())


def run():
    # scheduler = ScheduleFactory().get_instance()
    scheduler.add_job(try_trade, 'interval', seconds=TaskConfig.TRADING_INTERVAL_SECOND)
    scheduler.add_listener(task_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


def task_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')




if __name__ == '__main__':
    run()
