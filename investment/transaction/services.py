#  -*- coding:utf-8 -*-
from investment.transaction.handlers import transaction_handler
from datetime import datetime
import time
from investment.transaction.models import Trans_inst, Trans
from investment.enums import TransStatus, Platform, Symbol, ContractType
from investment.api.services import TransactionService


class ExpertAdvisorService:
    """
    智能交易服务
    """

    @staticmethod
    def start():
        """
        尝试发启交易
        """
        time.sleep(10)
        print('ea start: %s' % datetime.now())
        transaction_handler().try_trade()


class TransService(object):
    """
    交易服务类
    """
    db = None

    def __init__(self):
        self.db = Trans()

    def save_trans(self, trans):
        """
        保存订单
        :param trans_inst_id:
        :return:
        """
        self.db.save(trans)

    def save_trans_inst(self, trans_inst):
        """
        保存策略实例
        :param trans_inst_id:
        :return:
        """
        self.db.save(trans_inst)

    def _get_trans_by_db(self, trans_inst):
        """
         根据策略实例获得所有交易
        """
        _trans_inst_id = trans_inst.trans_inst_id
        _contract_type = trans_inst.contract_type
        results = self.db.select(trans_inst_id=_trans_inst_id)
        return results

    def get_synchro_trans(self, trans_inst):
        """
        获得最新交易信息，并同步数据库
        :param trans_inst:策略实例
        :return:
        """
        _trans_inst_id = trans_inst.trans_inst_id
        _symbol = trans_inst.symbol
        _user_id = trans_inst.user_id
        _trans = self._get_trans_by_db(trans_inst)
        for i, _tran in enumerate(_trans):
            _trans_id = _tran.trans_id
            _order_id = _tran.ex_trans_id
            data = TransactionService(Platform.PLATFORM_OKEX_FUTURE).get_order_by_ids(symbol=Symbol.get_symbol(_symbol),
                                                                                      contract_type=ContractType.QUARTER,
                                                                                      id=_order_id)
            if data and data["orders"]:
                _order = data["orders"][0]
                _amount = _order["amount"]  # 委托数量
                _fee = _order["fee"]  # 手续费
                _type = _order["type"]  # 订单类型
                _price_avg = _order["price_avg"]  # 平均价格
                _deal_amount = _order["deal_amount"]  # 成交数量
                _price = _order["price"]  # 订单价格
                _order_id = _order["order_id"]  # 订单id
                _status = _order["status"]  # 订单状态(0等待成交 1部分成交 2全部成交 -1撤单 4撤单处理中)
                _amt_left = _amount - _deal_amount
                self.db.save(trans_id=_trans_id, trans_inst_id=_trans_inst_id, ex_trans_id=_order_id, user_id=_user_id,
                             amt_left=_amt_left, e_status=_status, trans_amt=_amount, trans_price=_price,
                             deal_amt=_deal_amount, deal_price=_price_avg, symbol=_symbol, fee=_fee,
                             update_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


    def place(self, trans):
        """
        下单
        :param trans:订单
        :return:
        """
        _rs = TransactionService().place(trans.__dict__)
        _result = eval(_rs)["result"]
        _order_id = eval(_rs)["order_id"]
        if _result == True:
            trans.ex_trans_id = _order_id
            trans.e_status = TransStatus.NOT_STARTED.value
            self.save_trans(trans)
            return _order_id
        else:
            return None

    def cancel(self, order_id):
        """
        撤单
        :param trans:订单id
        :return:
        """
        _trans = self.db.select(ex_trans_ids=order_id)
        _rs = TransactionService().cancel(_trans.__dict__)
        _result = eval(_rs)["result"]
        if _result == True:
            _trans.e_status = TransStatus.WITHDRAWAL.value
            self.save_trans(_trans)
            return True
        else:
            return False


if __name__ == '__main__':
    a = ("a" == 1)
    b = ("abd" > "def")
    c = (123)
    c = b + c
    print(c)
