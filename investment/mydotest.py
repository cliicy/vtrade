import time,sys
from investment.api.handlers.fcoin_transaction_handler import FcoinTransactionHandler


if __name__ == '__main__':
    steps = int(sys.argv[1])
    # for test : query id information 10 times to check the consuming time
    fh = FcoinTransactionHandler()
    # 获取成交历史列表中的已经成交的订单信息
    # stime_begin = time.strftime('%H:%M:%S', time.localtime())
    # second1 = stime_begin.split(':')[2]
    stime_begin = time.time()
    print("开始时间：%s" %stime_begin)
    for index in range(steps):
        orders = fh.get_orders('xrpusdt', 'filled')

    # stime_end = time.strftime('%H:%M:%S', time.localtime())
    # second2 = stime_end.split(':')[2]
    stime_end = time.time()
    print("结束时间：%s" % stime_end)
    time_space = float(stime_end) - float(stime_begin)
    print('查询订单 %s 次所需时间：%s' % (steps,time_space))
