#  -*- coding:utf-8 -*-
from investment.synchronize.handlers.data_sync_handler import DataSyncHandler
class DataSyncService:
    """
    数据同步服务
    """
    def start_syn(self, platform, data_type, db_type):
        """
        开始同步数据
        :return:
        """
        print(platform)
        print(data_type)
        print(db_type)
        DataSyncHandler(platform, data_type, db_type).start()