#  -*- coding:utf-8 -*-
import asyncio
from investment.synchronize.services import *
import time
from investment.enums import Platform, PlatformDataType
import gevent, time
from gevent import monkey
from monitor.monitor.log.logger import Logger

logger = Logger(__name__).getlog()
now = lambda: time.time()
monkey.patch_all()  # 把当前程序中的所有io操作都做上标记


def save_data(**kwargs):
    """
    开启平台数据同步
    :param kwargs:{platform:平台， data_type:数据类型如kline， db_type:数据库类型如redis}
    :return:
    """
    start = now()
    logger.info("%s,%s,%s start:%s" % (kwargs['platform'], kwargs['data_type'], kwargs['db_type'], start))
    DataSyncService().start_syn(kwargs['platform'], kwargs['data_type'], kwargs['db_type'])


def run():
    tasks = []
    try:
        for name, platform in Platform.__members__.items():
            for type_name, data_type in PlatformDataType.__members__.items():
                tasks.append(gevent.spawn(save_data, platform=platform.value,
                                          data_type=data_type.value, db_type="redis"))
                tasks.append(gevent.spawn_later(0.001, save_data, platform=platform.value,
                                          data_type=data_type.value, db_type="mongo"))
        gevent.joinall(tasks)
    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    run()
