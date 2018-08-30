#  -*- coding:utf-8 -*-
from investment.enums import *
import json
import operator
import time
import re
class OkcoinDataConverter:
    """
    okcoin数据转换器
    """

    @staticmethod
    def convert(data_type, original_data):
        """
        原始数据转化成统一格式的数据
        :param PlatformDataType: 数据类型
        :param original_data: 原始数据
        :return:统一格式的数据
        """
        # print(original_data)
        # 统一格式数据
        formatted_data = []
        if data_type == PlatformDataType.PLATFORM_DATA_KLINE.value:
            # TODO kline数据转化..
            data = eval(original_data)
            # print(data)
            symbol = data[-1]
            rs_bch_usdt = data[0:len(data) - 1]
            for i in rs_bch_usdt:
                result = {}
                result["symbol"] = symbol
                result["ts"] = i[0]
                result["tm_intv"] = "1m"
                result["id"] = i[0]
                result["open"] = i[1]
                result["close"] = i[4]
                result["low"] = i[3]
                result["high"] = i[2]
                result["amount"] = ""
                result["vol"] = i[5]
                result["count"] = ""
                result['exchange'] = 'okex'
            formatted_data.append(result)
            # formatted_data = [original_data['s'], ]
            # if evt['channel'] == 'addChannel':
            #     pass
            # else:
            #     data = evt['data']
            #     for i in data:
            #         sym = '_'.join(evt['channel'].split('_')[3:5])
            #         symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX, sym)
            #         formatted_data_l = {'symbol':symbol,'ts':i[0], 'tm_intv':'1m',
            #                              'id':i[0],'open':i[1],'close':i[4],'low':i[3],'high':i[2],'amount':'','vol':i[5],'count':'','exchange':'okex'}
            #         formatted_data.append(formatted_data_l)
        elif data_type == PlatformDataType.PLATFORM_DATA_DEPTH.value:
            # TODO depth数据转化..
            original_data = json.loads(original_data)
            evt = original_data[0]
            if evt['channel'] == 'addChannel':
                pass
            else:
                sym = '_'.join(evt['channel'].split('_')[3:5])
                symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX, sym)
                ts = evt['data']['timestamp']
                # 卖方深度
                rs_eos_usdt_asks_1 = sorted(evt['data']['asks'], key=operator.itemgetter(0), reverse=False)
                rs_eos_usdt_asks = [[symbol] + [ts] + [i + 1] + value for i, value in enumerate(rs_eos_usdt_asks_1)]
                # 买方深度
                rs_eos_usdt_bids = evt['data']['bids']
                for i in range(len(rs_eos_usdt_bids)):
                    item1 = rs_eos_usdt_asks[i]
                    item2 = rs_eos_usdt_bids[i]
                    item3 = item1 + item2
                    formatted_data_l = {"symbol": item3[0],
                                         "ts": item3[1],
                                         "depth": item3[2],
                                         "sell_price": item3[3],
                                         "sell_amt": item3[4],
                                         "buy_price": item3[5],
                                         "buy_amt": item3[6],
                                         "exchange":'okex'
                                         }
                    formatted_data.append(formatted_data_l)

        elif data_type == PlatformDataType.PLATFORM_DATA_TICKER.value:
            # TODO ticker数据转化..
            original_data = json.loads(original_data)
            evt = original_data[0]
            if evt['channel'] == 'addChannel':
                pass
            else:
                sym = '_'.join(evt['channel'].split('_')[3:5])
                symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX, sym)
                formatted_data = [{'symbol':symbol,
                                   'ts':evt['data']['timestamp'],
                                   'latest_price':evt['data']['last'],
                                   'latest_amount':'',
                                   'max_buy1_price':evt['data']['buy'],
                                   'max_buy1_amt':'',
                                   'min_sell1_price':evt['data']['sell'],
                                   'min_sell1_amt':'',
                                   'pre_24h_price':'',
                                   'pre_24h_price_max':evt['data']['high'],
                                   'pre_24h_price_min':evt['data']['low'],
                                   'pre_24h_bt_finish_amt':evt['data']['vol'],
                                   'pre_24h_usd_finish_amt':'',
                                   'exchange': 'okex'
                                   }]
        elif data_type == PlatformDataType.PLATFORM_DATA_TRADE.value:
            # TODO trade数据转化..
            original_data = json.loads(original_data)
            evt = original_data[0]
            data = evt['data']
            write_lines=[]
            today_date_zh = time.strftime("%Y-%m-%d")
            for i in data:
                sym = '_'.join(evt['channel'].split('_')[3:5])
                symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX, sym)

                formatted_data_l = {"symbol":symbol,
                                   "id":i[0],
                                   "ts":int(time.mktime(time.strptime(today_date_zh + ' ' + i[3], '%Y-%m-%d %H:%M:%S'))) * 1000,
                                   "direction":i[4],
                                   "amount":i[2],
                                   "price":i[1],
                                   "exchange": 'okex'
                                   }
                formatted_data.append(formatted_data_l)
            # formatted_data = write_lines
        return formatted_data

class OkcoinFutureDataConverter:
    """
    okex 合约数据转换器
    """

    @staticmethod
    def convert(data_type, original_data):
        """
        原始数据转化成统一格式的数据
        :param PlatformDataType: 数据类型
        :param original_data: 原始数据
        :return:统一格式的数据
        """


        # 统一格式数据
        formatted_data = []
        if data_type == PlatformDataType.PLATFORM_DATA_KLINE.value:
            # TODO kline数据转化..
            # formatted_data = [original_data['s'], ]
            '''
            返回值说明
            [时间 ,开盘价,  最高价,  最低价, 收盘价,成交量(张),成交量(币)]
            [string, string, string, string, string, string]
            '''
            data = eval(original_data)
            # print(data)
            symbol = data[-2]
            contractType = data[-1]
            rs_bch_usdt = data[0:len(data) - 2]
            for i in rs_bch_usdt:
                result = {}
                result['symbol'] = symbol
                result['ts'] = i[0]
                result['tm_intv'] = '1m'
                result['id'] = i[0]
                result['open'] = i[1]
                result['close'] = i[4]
                result['low'] = i[3]
                result['high'] = i[2]
                result['amount'] = ''
                result['vol'] = i[6]
                result['count'] = i[5]
                result['contractType'] = contractType
                result['exchange'] = 'okex_future'
            formatted_data.append(result)

        elif data_type == PlatformDataType.PLATFORM_DATA_DEPTH.value:
            # TODO depth数据转化..
            '''
            返回值说明
            timestamp(long): 服务器时间戳
            asks(array):卖单深度 数组索引(string) 0 价格, 1 量(张), 2 量(币) ,3 累计量(币) ,4 累计量(张)
                                                  [63.968,  2,       0.3126,     545.9305,  3487]
            bids(array):买单深度 数组索引(string) 0 价格, 1 量(张), 2 量(币) 3, 累计量(币) ,4 累计量(张)
            [[symbol] + [ts] + [i],63.916,36,5.6323,389.0821,2484,63.627,250,39.2914,39.2914,250]
               0          1     2    3    4   5      6        7    8      9    10      11     12
            '''
            original_data = json.loads(original_data)
            evt = original_data[0]
            if evt['channel'] == 'addChannel':
                pass
            else:
                sym = re.match('.*_future(.*)_depth.*', evt['channel']).group(1)
                symbol_get = '_'.join(sym.split('_')[::-1])
                symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX_FUTURE, symbol_get)
                contractType = re.match('.*_depth_(.*)_20', evt['channel']).group(1)
                ts = evt['data']['timestamp']
                # 卖方深度 先排序 reverse=False 升序
                rs_eos_usdt_asks_1 = sorted(evt['data']['asks'], key=operator.itemgetter(0), reverse=False)
                rs_eos_usdt_asks = [[symbol] + [ts] + [i+1] + value for i, value in enumerate(rs_eos_usdt_asks_1)]
                # 买方深度
                rs_eos_usdt_bids = evt['data']['bids']
                for i in range(len(rs_eos_usdt_asks)):
                    item1 = rs_eos_usdt_asks[i]
                    item2 = rs_eos_usdt_bids[i]
                    item3 = item1 + item2
                    formatted_data_l = {"symbol": item3[0],
                                         "ts": item3[1],
                                         "depth": item3[2],
                                         "sell_price": item3[3],
                                         "sell_amt": item3[5],
                                         "sell_amt_cont": item3[4],
                                         "sell_count_amt": item3[6],
                                         "sell_count_amt_cont": item3[7],
                                         "buy_price": item3[8],
                                         "buy_amt": item3[10],
                                         "buy_amt_cont": item3[9],
                                         "buy_count_amt": item3[11],
                                         "buy_count_amt_cont": item3[12],
                                         "contractType":contractType,
                                         "exchange":'okex_future'
                                         }
                    formatted_data.append(formatted_data_l)

        elif data_type == PlatformDataType.PLATFORM_DATA_TICKER.value:
            # TODO ticker数据转化..
            '''
            返回值说明
            limitHigh(string):最高买入限制价格
            limitLow(string):最低卖出限制价格
            vol(double):24小时成交量
            sell(double):卖一价格
            buy(double): 买一价格
            unitAmount(double):合约价值
            hold_amount(double):当前持仓量
            contractId(long):合约ID
            high(double):24小时最高价格
            low(double):24小时最低价格

            '''
            original_data = json.loads(original_data)
            evt = original_data[0]
            if evt['channel'] == 'addChannel':
                pass
            else:
                result = {}
                sym = re.match('.*_future(.*)_ticker.*', evt['channel']).group(1)
                symbol_get = '_'.join(sym.split('_')[::-1])
                symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX_FUTURE, symbol_get)

                result['symbol'] = symbol
                result['ts'] = int(time.time() * 1000)
                result['latest_price'] = evt['data']['last']
                result['latest_amount'] = ''
                result['max_buy1_price'] = evt['data']['buy']
                result['max_buy1_amt'] = ''
                result['min_sell1_price'] = evt['data']['sell']
                result['min_sell1_amt'] = ''
                result['pre_24h_price'] = ''
                result['pre_24h_price_max'] = evt['data']['high']
                result['pre_24h_price_min'] = evt['data']['low']
                result['pre_24h_bt_finish_amt'] = evt['data']['vol']
                result['pre_24h_usd_finish_amt'] = ''
                result['limitHigh'] = evt['data']['limitHigh']
                result['limitLow'] = evt['data']['limitLow']
                result['unitAmount'] = evt['data']['unitAmount']
                result['hold_amount'] = evt['data']['hold_amount']
                result['contractId'] = evt['data']['contractId']
                result['contractType'] = re.match('.*_ticker_(.*)', evt['channel']).group(1)
                result['exchange'] = 'okex_future'
                formatted_data = [result]

        elif data_type == PlatformDataType.PLATFORM_DATA_TRADE.value:
            # TODO trade数据转化..
            '''
            返回值说明
            [交易序号, 价格, 成交量(张), 时间, 买卖类型]
            [string,  string, string,   string, string,]

            '''
            original_data = json.loads(original_data)
            evt = original_data[0]
            data = evt['data']
            write_lines=[]
            today_date_zh = time.strftime("%Y-%m-%d")
            for i in data:
                sym = re.match('.*_future(.*)_trade.*', evt['channel']).group(1)
                symbol_get = '_'.join(sym.split('_')[::-1])
                symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX_FUTURE, symbol_get)

                formatted_data_l = {"symbol":symbol,
                                   "id":i[0],
                                   "ts":i[3],
                                   "direction":i[4],
                                   "amount":i[2],
                                   "price":i[1],
                                   "contractType": re.match('.*_trade_(.*)', evt['channel']).group(1),
                                   "exchange": 'okex_future'
                                   }
                formatted_data.append(formatted_data_l)
            # formatted_data = write_lines
        return formatted_data