#  -*- coding:utf-8 -*-
from management.info.models import Account
class EarlyWarningService:
    """
    预警处理类
    """
    def check_up(self, **kwargs):
        """
        检查用户的策略收益情况
        :param kwargs:
        :return:
        """