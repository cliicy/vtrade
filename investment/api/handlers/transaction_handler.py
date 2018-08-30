#  -*- coding:utf-8 -*-
class TransactionHandler:
    """
    抽象的处理交易的通信控制器
    1.根据setting拼装请求参数
    2.调用communicators发起请求
    3.返回结果给services
    """

    def place(self, **args):
        """
        下单
        """
        pass

    def cancel(self, **args):
        """
        撤单
        """
        pass

    def get_order(self, **args):
        """
        查询订单信息
        """
        pass

    def get_match_results(self, **args):
        """
        查询订单的成交明细
        """
        pass
