#  -*- coding:utf-8 -*-
from investment.enums import PlatformDataType, Symbol, Platform

class BinanceDataConverter:
    """
    币安数据转换器
    """

    @staticmethod
    def convert(data_type, original_data):
        """
        原始数据转化成统一格式的数据
        :param PlatformDataType: 数据类型
        :param original_data: 原始数据
        :return:统一格式的数据
        """
        original_data = eval(original_data)
        sym = Symbol.convert_to_standard_symbol(Platform.PLATFORM_BINANCE, original_data['s'])
        # sym_tick = Symbol.convert_to_standard_symbol(Platform.PLATFORM_BINANCE, original_data[i]['s'])
        # 统一格式数据
        formatted_data = ""
        if data_type == PlatformDataType.PLATFORM_DATA_KLINE.value:
            formatted_dict = {}
            formatted_dict["symbol"] = sym
            formatted_dict["ts"] = original_data['k']['T']
            formatted_dict["tm_intv"] =original_data['k']['i']
            formatted_dict["id"] = original_data['k']['t']
            formatted_dict["open"] = original_data['k']['o']
            formatted_dict["close"] = original_data['k']['c']
            formatted_dict["low"] = original_data['k']['l']
            formatted_dict["high"] = original_data['k']['h']
            formatted_dict["amount"] = original_data['k']['v']
            formatted_dict["vol"] = original_data['k']['q']
            formatted_dict["count"] = original_data['k']['n']
            formatted_dict["exchange"] = "bian"

            formatted_data = [formatted_dict]
        elif data_type == PlatformDataType.PLATFORM_DATA_DEPTH.value:
            # depth数据转化..
            #print(original_data)
            # symbol=original_data['s']
            ts=original_data['E']
            write_lines = []
            bids = original_data['b']
            asks = original_data['a']
            if not asks:
                for i in range(len(bids)):
                    depth = i+1
                    buy_price = bids[i][0]
                    buy_amt = bids[i][1]
                    formatted_depth = {}
                    formatted_depth['symbol'] = sym
                    formatted_depth['ts'] = ts
                    formatted_depth['depth'] = depth
                    formatted_depth['sell_price'] = ''
                    formatted_depth['sell_amt'] = ''
                    formatted_depth['buy_price'] = buy_price
                    formatted_depth['buy_amt'] = buy_amt
                    formatted_depth['exchange'] = 'bian'
                    write_lines.append(formatted_depth)
            # 判断b为空的情况
            elif not bids:
                for j in range(len(asks)):
                    depth = j +1
                    sell_price = asks[j][0]
                    sell_amt = asks[j][1]
                    formatted_depth = {}
                    formatted_depth['symbol'] = sym
                    formatted_depth['ts'] = ts
                    formatted_depth['depth'] = depth
                    formatted_depth['sell_price'] = sell_price
                    formatted_depth['sell_amt'] = sell_amt
                    formatted_depth['buy_price'] = ''
                    formatted_depth['buy_amt'] = ''
                    formatted_depth['exchange'] = 'bian'
                    write_lines.append(formatted_depth)
            else:
                # a b 都不为空的情况 再分两种情况1 a b 相等 2 a b不相等
                small_len = len(asks)
                if small_len > len(bids):
                    small_len = len(bids)
                for i in range(small_len):
                    depth = i +1
                    sell_price = asks[i][0]
                    sell_amt = asks [i][1]
                    buy_price = bids[i][0]
                    buy_amt = bids[i][0]
                    formatted_depth = {}
                    formatted_depth['symbol'] = sym
                    formatted_depth['ts'] = ts
                    formatted_depth['depth'] = depth
                    formatted_depth['sell_price'] = sell_price
                    formatted_depth['sell_amt'] =  sell_amt
                    formatted_depth['buy_price'] = buy_price
                    formatted_depth['buy_amt'] = buy_amt
                    formatted_depth['exchange'] = 'bian'
                    write_lines.append(formatted_depth)
                if len(asks) > small_len:
                    for j in range(small_len, len(bids)):
                        formatted_depth = {}
                        formatted_depth['symbol'] = sym
                        formatted_depth['ts'] = ts
                        formatted_depth['depth'] = j + 1
                        formatted_depth['sell_price'] = asks[j][0]
                        formatted_depth['sell_amt'] = asks[j][1]
                        formatted_depth['buy_price'] = ''
                        formatted_depth['buy_amt'] = ''
                        formatted_depth['exchange'] = 'bian'
                        write_lines.append(formatted_depth)
                if len(bids) > small_len:
                    for k in range(small_len, len(bids)):
                        formatted_depth = {}
                        formatted_depth['symbol'] = sym
                        formatted_depth['ts'] = ts
                        formatted_depth['depth'] = k + 1
                        formatted_depth['sell_price'] = ''
                        formatted_depth['sell_amt'] = ''
                        formatted_depth['buy_price'] = bids[k][0]
                        formatted_depth['buy_amt'] = bids[k][1]
                        formatted_depth['exchange'] = 'bian'
                        write_lines.append(formatted_depth)
            formatted_data = write_lines
        elif data_type == PlatformDataType.PLATFORM_DATA_TICKER.value:
            # ticker数据转化
            formatted_ticker = {}
            for i in range(len(original_data)):
                formatted_ticker["symbol"] = Symbol.convert_to_standard_symbol(Platform.PLATFORM_BINANCE, original_data[i]['s'])
                formatted_ticker["ts"] = original_data[i]['E']
                formatted_ticker["latest_price"] = ''
                formatted_ticker["lastest_amount"] =''
                formatted_ticker["max_buy1_price"] = original_data[i]['b']
                formatted_ticker["max_buy1_amt"] = original_data[i]['B']
                formatted_ticker["min_sell1_price"] = original_data[i]['a']
                formatted_ticker["min_sell1_amt"] = original_data[i]['A']
                formatted_ticker["pre_24h_price"] = ''
                formatted_ticker["pre_24h_price_max"] = original_data[i]['h']
                formatted_ticker["pre_24h_price_min"] = original_data[i]['l']
                formatted_ticker["pre_24h_bt_finish_amt"] = original_data[i]['v']
                formatted_ticker["pre_24h_usd_finish_amt"] = original_data[i]['q']
            formatted_data = [formatted_ticker]
        elif data_type == PlatformDataType.PLATFORM_DATA_TRADE.value:
            # trade数据转化
            formatted_trade = {}
            formatted_trade['symbol'] = sym
            formatted_trade['id'] = original_data['t']
            formatted_trade['ts'] = original_data['T']
            formatted_trade['direction'] = ''
            formatted_trade['amount'] = original_data['q']
            formatted_trade['price'] = original_data['p']
            formatted_trade['exchange'] = "bian"

            formatted_data = [formatted_trade]
            # print(original_data['p'])

        print(formatted_data)
        return formatted_data
