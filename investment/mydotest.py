import datetime,time
from api.handlers.fcoin_transaction_handler import FcoinTransactionHandler
from enums import Symbol,ContractType, Platform,OKEX_SYMBOL_LIST,OKEX_FUTURE_SYMBOL_LIST


if __name__ == '__main__':
    # for test : query id information 10 times to check the consuming time
    fh = FcoinTransactionHandler()
    # 获取成交历史列表中的已经成交的订单信息
    stime_begin = time.strftime('%H:%M:%S', time.localtime())
    second1 = stime_begin.split(':')[2]
    print("开始时间：%s" %second1)
    for index in range(10):
        orders = fh.get_orders('xrpusdt', 'filled')

    stime_end = time.strftime('%H:%M:%S', time.localtime())
    second2 = stime_end.split(':')[2]
    print("结束时间：%s" % second2)
    time_space = float(second2) - float(second1)
    print('查询订单10次所需时间：%s' % time_space)
