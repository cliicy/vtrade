#  -*- coding:utf-8 -*-
from investment.enums import Platform, PlatformDataType, PlatformDataTypeIndex, Symbol, ContractType
from investment.api.handlers.fcoin_transaction_handler import FcoinTransactionHandler
from investment.api.handlers.okex_transaction_handler import OkexTransactionHandler
from investment.api.handlers.okex_future_transaction_handler import OkexFutureTransactionHandler
import redis
import time
import datetime
from config import DBConfig as Config


class TransactionService(object):
    """
    交易服务
    1.根据传入参数判断交易所
    2.返回结果
    """
    trading_platform = None
    # redis
    _redis = None
    pool = None

    def __init__(self, trading_platform):
        self.trading_platform = trading_platform

    def place(self, **kwargs):
        """
        下单
        :return:
        """
        if ("symbol" in kwargs):
            _symbol = kwargs["symbol"]
        if ("contract_type" in kwargs):
            _contract_type = kwargs["contract_type"]
        if ("price" in kwargs):
            _price = kwargs["price"]
        if ("amount" in kwargs):
            _amount = kwargs["amount"]
        if ("trade_type" in kwargs):
            _trade_type = kwargs["trade_type"]
        # if self.trading_platform == "huobi":
        #     HuobiTransactionHandler.place(self, **args)
        # if self.trading_platform == "bian":
        #     BianTransactionHandler.place(self, **args)
        # if self.trading_platform == "fcoin":
        #     FcoinTransactionHandler.place(self, **args)
        if self.trading_platform == Platform.PLATFORM_OKEX:
            return OkexTransactionHandler().place(_symbol, _trade_type, _price, _amount)
        elif self.trading_platform == Platform.PLATFORM_OKEX_FUTURE:
            return OkexFutureTransactionHandler().place(_symbol, _contract_type, _price, _amount, _trade_type)

    def cancel(self, **kwargs):
        """
        撤单
        :return:
        """
        if ("symbol" in kwargs):
            _symbol = kwargs["symbol"]
        if ("contract_type" in kwargs):
            _contract_type = kwargs["contract_type"]
        if ("order_id" in kwargs):
            _order_id = kwargs["order_id"]
        # if self.trading_platform == "huobi":
        #     HuobiTransactionHandler.cancel(self, **args)
        # if self.trading_platform == "bian":
        #     BianTransactionHandler.cancel(self, **args)
        # if self.trading_platform == "fcoin":
        #     FcoinTransactionHandler(self, **args)
        if self.trading_platform == Platform.PLATFORM_OKEX:
            return OkexTransactionHandler().cancel(_symbol, _order_id)
        if self.trading_platform == Platform.PLATFORM_OKEX_FUTURE:
            return OkexFutureTransactionHandler().cancel(_symbol, _contract_type, _order_id)

    def get_order(self, **kwargs):
        """
        获得订单信息
        :return:
        """
        if ("symbol" in kwargs):
            _symbol = kwargs["symbol"]
            # _symbol = Symbol.get_platform_symbol(self.trading_platform, _symbol)
        if ("contract_type" in kwargs):
            _contract_type = kwargs["contract_type"].value
        if ("order_id" in kwargs):
            _order_id = kwargs["order_id"]
        if ("status" in kwargs):
            _status = kwargs["status"]
        if ("current_page" in kwargs):
            _current_page = kwargs["current_page"]
        else:
            _current_page = 1
        if ("page_length" in kwargs):
            _page_length = kwargs["page_length"]
        else:
            _page_length = 50
        _order_info = None
        # if self.trading_platform == "huobi":
        #     HuobiTransactionHandler.get_order(self, **args)
        # if self.trading_platform == "bian":
        #     BianTransactionHandler.get_order(self, **args)
        # if self.trading_platform == "fcoin":
        #     FcoinTransactionHandler.get_order(self, **args)
        if self.trading_platform == Platform.PLATFORM_OKEX:
            OkexTransactionHandler.get_order(self, **kwargs)
        if self.trading_platform == Platform.PLATFORM_OKEX_FUTURE:
            _order_info = self.__get_order(_symbol, _contract_type, _order_id,
                                           _status, _current_page, _page_length)
        print(_order_info)
        return _order_info

    def __get_order(self, symbol, contract_type, order_id, status, current_page, page_length,
                    order_info={"orders": None}):
        """
        获得所有翻页后的订单详情
        :param symbol:
        :param contract_type:
        :param order_id:
        :param status:
        :param current_page:
        :param page_length:
        :param order_info:
        :return:
        """
        __order_info = OkexFutureTransactionHandler().get_order(symbol, contract_type, order_id,
                                                                status, current_page, page_length)
        __original_orders = order_info["orders"]
        __new_orders = __order_info["orders"]

        if __new_orders:
            if __original_orders:
                __original_orders.append(__new_orders)
            else:
                __original_orders = __new_orders

            __order_info["orders"] = __original_orders
            if len(__new_orders) < 50:
                return __order_info
            else:
                current_page += 1
                self.__get_order(self, symbol, contract_type, order_id, status, current_page, page_length, __order_info)

        return __order_info

    def get_order_by_ids(self, symbol, contract_type, ids):
        """
        根据id获得订单信息
        :param id:
        :return:
        """
        return self.__get_order_by_id(symbol, contract_type, ids)

    def __get_order_by_id(self, symbol, contract_type, id, order_info={"orders": None}):
        """
        根据id获得50条订单信息
        :param id:
        :return:
        """
        print("ids=", id)
        ids = id.split(",")
        next_ids = None
        if len(ids) > 50:
            order_ids = ','.join(ids[0:50])
            next_ids = ','.join(ids[50:])
        else:
            order_ids = id
        # 批量查询订单信息
        __order_info = OkexFutureTransactionHandler().get_order_s(symbol, contract_type, order_ids)
        __original_orders = order_info["orders"]
        __new_orders = __order_info["orders"]
        if __new_orders:
            if __original_orders:
                __original_orders.append(__new_orders)
            else:
                __original_orders = __new_orders
            __order_info["orders"] = __original_orders
        else:
            __order_info = order_info

        if next_ids:
            self.__get_order_by_id(symbol, contract_type, next_ids, __order_info)

        return __order_info

    def get_trans_inst(self, **kwargs):
        """
        查询策略实例
        :param kwargs:
        :return:
        """
        if ("trans_inst" in kwargs):
            _trans_inst = kwargs["trans_inst"]
        if ("tran_strategy_id" in kwargs):
            _tran_strategy_id = kwargs["tran_strategy_id"]
        if ("user_id" in kwargs):
            _user_id = kwargs["user_id"]
        if ("symbol" in kwargs):
            _symbol = kwargs["symbol"]
        if ("exchange_ids" in kwargs):
            _exchange_ids = kwargs["exchange_ids"]
        # 1.查询所有策略实例
        # 2.查询所有策略实例对应该的交易

    def get_match_results(self, **kwargs):
        """
        获得订单交易信息
        :return:
        """
        # if self.trading_platform == "huobi":
        #     HuobiTransactionHandler.get_match_results(self, **args)
        # if self.trading_platform == "bian":
        #     BianTransactionHandler.get_match_results(self, **args)
        # if self.trading_platform == "fcoin":
        #     FcoinTransactionHandler.get_match_results(self, **args)
        if self.trading_platform == Platform.PLATFORM_OKEX:
            OkexTransactionHandler.get_match_results(self, **kwargs)
        if self.trading_platform == Platform.PLATFORM_OKEX_FUTURE:
            OkexFutureTransactionHandler.get_match_results(self, **kwargs)

    def get_account_info(self, **kwargs):
        """
        用户当前信息查询
        :param kwargs:
        :return:
        """
        if self.trading_platform == Platform.PLATFORM_OKEX:
            return OkexTransactionHandler().get_account_info()
        if self.trading_platform == Platform.PLATFORM_OKEX_FUTURE:
            return OkexFutureTransactionHandler().get_account_info()
        if self.trading_platform == Platform.PLATFORM_FCOIN:
            return FcoinTransactionHandler().get_account_info()

    def get_kline_info(self, **kwargs):
        """
        当前kline信息查询
        :param kwargs:
        :return:
        """
        # TODO 其它交易所待补充
        if self.trading_platform == Platform.PLATFORM_OKEX_FUTURE:
            # return OkexFutureTransactionHandler().get_kline_info(self)
            okexfu = OkexFutureTransactionHandler()
            _symbol_get = None
            if ("symbol_get" in kwargs):
                _symbol_get = kwargs["symbol_get"]
            this_week = okexfu.get_kline_info(_symbol_get, ContractType.THIS_WEEK.value, size=60 + 1)
            next_week = okexfu.get_kline_info(_symbol_get, ContractType.NEXT_WEEK.value, size=60 + 1)
            quarter = okexfu.get_kline_info(_symbol_get, ContractType.QUARTER.value, size=60 + 1)
            _kline_info = dict(this_week=this_week, next_week=next_week, quarter=quarter)
            print(_kline_info)
            return _kline_info

    def get_trades_info(self, **kwargs):
        """
        当前kline信息查询
        :param kwargs:
        :return:
        """
        # TODO 其它交易所待补充
        if self.trading_platform == Platform.PLATFORM_OKEX_FUTURE:
            _symbol_get = None
            _contract_type = None
            if ("symbol_get" in kwargs):
                _symbol_get = kwargs["symbol_get"]
            if ("contract_type" in kwargs):
                _contract_type = kwargs["contract_type"]
            rest_start_time = time.mktime(datetime.datetime.now().timetuple())
            _trades_info = OkexFutureTransactionHandler().get_trades_info(_symbol_get, _contract_type)
            print(_trades_info)
            rest_end_time = time.mktime(datetime.datetime.now().timetuple())
            print(rest_end_time - rest_start_time)
            # print(time.mktime(datetime.datetime.now().timetuple()) - _trades_info["date"])
            # print(time.time() * 1000 - _trades_info["date_ms"])
            if (rest_end_time - rest_start_time > 1):
                key = f'{Symbol.get_standard_symbol(_symbol_get)}.*.{_contract_type.value}'
                index = PlatformDataTypeIndex.getIndex(self.trading_platform,
                                                       PlatformDataType.PLATFORM_DATA_TRADE.value)
                # 查询redis最新数据
                self._redis = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=index)
                trade_cache = self._redis.keys(key)
                if trade_cache:
                    trade_cache.sort(reverse=True)
                    print(trade_cache[0])
                    max_cache_id = str(trade_cache[0]).split(".")[1]
                    print(max_cache_id)
                    print(_trades_info["tid"])
                    # 比较id取最近数据
                    if int(max_cache_id) > _trades_info["tid"]:
                        return self._redis.get(trade_cache)

        return _trades_info

    def get_ticker_info(self, **kwargs):
        """
        当前ticker信息查询
        :param kwargs:
        :return:
        """
        # TODO 其它交易所待补充
        if self.trading_platform == Platform.PLATFORM_OKEX:
            _symbol_get = None
            _contract_type = None
            if ("symbol_get" in kwargs):
                _symbol_get = kwargs["symbol_get"]
            rest_start_time = time.mktime(datetime.datetime.now().timetuple())
            _ticker_info = OkexTransactionHandler().get_ticker_info(_symbol_get)
            print(_ticker_info)
            rest_end_time = time.mktime(datetime.datetime.now().timetuple())
            print(rest_end_time - rest_start_time)
            # print(time.mktime(datetime.datetime.now().timetuple()) - _trades_info["date"])
            # print(time.time() * 1000 - _trades_info["date_ms"])
            if (rest_end_time - rest_start_time > 1):
                key = f'{Symbol.get_standard_symbol(_symbol_get)}.*'
                index = PlatformDataTypeIndex.getIndex(self.trading_platform,
                                                       PlatformDataType.PLATFORM_DATA_TICKER.value)
                # 查询redis最新数据
                self._redis = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=index)
                trade_cache = self._redis.keys(key)
                if trade_cache:
                    trade_cache.sort(reverse=True)
                    print(trade_cache[0])
                    max_cache_id = str(trade_cache[0]).split(".")[1]
                    print(max_cache_id)
                    print(_ticker_info["tid"])
                    # 比较id取最近数据
                    if int(max_cache_id) > _ticker_info["tid"]:
                        return self._redis.get(trade_cache)
        elif self.trading_platform == Platform.PLATFORM_OKEX_FUTURE:
            _symbol_get = None
            _contract_type = None
            if ("symbol_get" in kwargs):
                _symbol_get = kwargs["symbol_get"]
            if ("contract_type" in kwargs):
                _contract_type = kwargs["contract_type"]
            rest_start_time = time.mktime(datetime.datetime.now().timetuple())
            _ticker_info = OkexFutureTransactionHandler().get_future_ticker_info(_symbol_get, _contract_type)
            print(_ticker_info)
            rest_end_time = time.mktime(datetime.datetime.now().timetuple())
            print(rest_end_time - rest_start_time)
            # print(time.mktime(datetime.datetime.now().timetuple()) - _trades_info["date"])
            # print(time.time() * 1000 - _trades_info["date_ms"])
            if (rest_end_time - rest_start_time > 1):
                key = f'{Symbol.get_standard_symbol(_symbol_get)}.*.{_contract_type.value}'
                index = PlatformDataTypeIndex.getIndex(self.trading_platform,
                                                       PlatformDataType.PLATFORM_DATA_TICKER.value)
                # 查询redis最新数据
                self._redis = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=index)
                trade_cache = self._redis.keys(key)
                if trade_cache:
                    trade_cache.sort(reverse=True)
                    print(trade_cache[0])
                    max_cache_id = str(trade_cache[0]).split(".")[1]
                    print(max_cache_id)
                    print(_ticker_info["tid"])
                    # 比较id取最近数据
                    if int(max_cache_id) > _ticker_info["tid"]:
                        return self._redis.get(trade_cache)

        return _ticker_info

    # TODO
    def get_depth_info(self, **kwargs):
        """
        当前kline信息查询
        :param kwargs:
        :return:
        """
        pass

    # TODO
    def get_future_index(self,  **kwargs):
        """
        OKex期货指数
        :param symbol:币对枚举
        :return:
        """
        symbol = kwargs["symbol_get"]
        return OkexFutureTransactionHandler().get_future_index(symbol)

    def get_exchange_rate(self):
        """
        获取美元人民币汇率
        :return:
        """
        return OkexFutureTransactionHandler().get_exchange_rate()


class SmsService:
    """
    短信服务类
    """


class EmailService:
    """
    邮件服务类
    """


if __name__ == '__main__':
    # data = RealTimeInquiry(Platform.PLATFORM_OKEX_FUTURE).get_trades_info(symbol_get=Symbol.BCH_USDT, contract_type=ContractType.THIS_WEEK)
    # print(data)
    # data = TransactionService(Platform.PLATFORM_OKEX_FUTURE).get_order(symbol=Symbol.EOS_USDT,
    #                                                                    contract_type=ContractType.QUARTER,
    #                                                                    order_id='-1', status='2')
    # print(data)
    # data = TransactionService(Platform.PLATFORM_OKEX_FUTURE).get_kline_info(symbol_get=Symbol.BCH_USDT)
    # print(data)
    # id = '1350984687039488, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc,' \
    #      ' aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc,' \
    #      ' aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc,' \
    #      ' aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc,' \
    #      ' aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc,' \
    #      ' aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc,' \
    #      ' aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc,' \
    #      ' aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc,' \
    #      ' aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc, aaaa, bbbbbbbb, ccccccc,' \
    #      '1352567882597376,1352567344346112'
    # print(id[3:])
    # data = TransactionService(Platform.PLATFORM_OKEX_FUTURE).get_order_by_id(symbol=Symbol.EOS_USDT,
    #                                                                          contract_type=ContractType.QUARTER, id=id)
    data = TransactionService(Platform.PLATFORM_OKEX).get_ticker_info(symbol_get=Symbol.EOS_USDT)
    # print(TransactionService(Platform.PLATFORM_OKEX_FUTURE).get_exchange_rate())

