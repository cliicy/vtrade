#  -*- coding:utf-8 -*-
from datetime import datetime
from investment.api.services import TransactionService


class TransactionHandler:
    """
    交易处理类
    """

    def try_trade(self):
        """
        尝试发启交易
        """
        print('try trade start: %s' % datetime.now())
        # 1.根据策略判定是否发启交易，获得发启交易的属性
        # TODO opportunity_judge
        # 2.发启交易请求
        # TODO start_trading
        # 3.记录交易数据
        # TODO record_bill

    def opportunity_judge(self):
        """
        根据策略判定是否发启交易，发启交易的属性
        """
        # TODO

    def start_trading(self):
        """
        发启交易
        :return:
        """
        # TODO 调用 investment.api.services.TransactionService进行交易

    def record_bill(self):
        """
        记录交易数据
        :return:
        """
        # TODO
