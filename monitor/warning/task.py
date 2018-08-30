from datetime import datetime
import asyncio
from investment.transaction.services import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import TaskConfig
scheduler = AsyncIOScheduler()


@asyncio.coroutine
def try_trade():
    ExpertAdvisorService.try_trade()
    print('Tick! The time is: %s' % datetime.now())


def run():
    scheduler.add_job(try_trade, 'interval', seconds=TaskConfig.RISK_WARNING_INTERVAL_SECOND)
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    run()
