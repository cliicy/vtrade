#  -*- coding:utf-8 -*-
from investment.enums import PlatformDataType, Symbol, Platform

class HuobiDataConverter:
    """
    火币数据转换器
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
        # 统一格式数据
        formatted_data = ""
        if data_type == PlatformDataType.PLATFORM_DATA_KLINE.value:
            #返回列表数据 列表中每一项为一个字典类型
            formatted_dict ={}
            formatted_dict["symbol"] = Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI,original_data["ch"].split('.')[1])
            formatted_dict["ts"] = original_data['ts']
            formatted_dict["tm_intv"] = '1m'
            formatted_dict["id"] = original_data['tick']['id']
            formatted_dict["open"] = original_data['tick']['open']
            formatted_dict["close"] = original_data['tick']['close']
            formatted_dict["low"] = original_data['tick']['low']
            formatted_dict["high"] = original_data['tick']['high']
            formatted_dict["amount"] = original_data['tick']['amount']
            formatted_dict["vol"] =  original_data['tick']['vol']
            formatted_dict["count"] =  original_data['tick']['count']
            formatted_dict["exchange"] = "huobi"
            # 返回列表，列表中的每一项为要插入数据库的数据字典记录
            formatted_data = [formatted_dict]

        elif data_type == PlatformDataType.PLATFORM_DATA_DEPTH.value:
            #返回列表，列表中的每一项为要插入数据库的数据字典记录
            symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI,original_data["ch"].split('.')[1])
            ts = original_data['ts']
            write_lines = []
            bids = original_data['tick']['bids']
            # print (len(bids))
            asks = original_data['tick']['asks']
            # print(len(asks))
            #处理买入价与卖出价数量不同时，记录的整理方式方法
            small_len = len(bids)
            if small_len > len(asks):
                small_len = len(asks)
            for i in range(small_len):
                depth = i + 1
                sell_price = asks[i][0]
                sell_amt = asks[i][1]
                buy_price = bids[i][0]
                buy_amt = bids[i][1]
                formatted_dict = {}
                formatted_dict["symbol"] = symbol
                formatted_dict["ts"] = ts
                formatted_dict["depth"] = depth
                formatted_dict["sell_price"] = sell_price
                formatted_dict["sell_amt"] = sell_amt
                formatted_dict["buy_price"] = buy_price
                formatted_dict["buy_amt"] = buy_amt
                formatted_dict["exchange"] = "huobi"

                write_lines.append(formatted_dict)
            if len(bids) > small_len:
                for j in range(small_len, len(bids)):
                    depth = j + 1
                    buy_price = bids[j][0]
                    buy_amt = bids[j][1]
                    formatted_dict = {}
                    formatted_dict["symbol"] = symbol
                    formatted_dict["ts"] = ts
                    formatted_dict["depth"] = depth
                    formatted_dict["sell_price"] = ''
                    formatted_dict["sell_amt"] = ''
                    formatted_dict["buy_price"] = buy_price
                    formatted_dict["buy_amt"] = buy_amt
                    formatted_dict["exchange"] = "huobi"

                    write_lines.append(formatted_dict)
            if len(asks) > small_len:
                for k in range(small_len, len(asks)):
                    depth = k + 1
                    sell_price = asks[k][0]
                    sell_amt = asks[k][1]
                    formatted_dict = {}
                    formatted_dict["symbol"] = symbol
                    formatted_dict["ts"] = ts
                    formatted_dict["depth"] = depth
                    formatted_dict["sell_price"] = sell_price
                    formatted_dict["sell_amt"] = sell_amt
                    formatted_dict["buy_price"] = ''
                    formatted_dict["buy_amt"] = ''
                    formatted_dict["exchange"] = "huobi"

                    write_lines.append(formatted_dict)

            formatted_data = write_lines
        elif data_type == PlatformDataType.PLATFORM_DATA_TICKER.value:
            formatted_dict = {}
            formatted_dict['symbol'] = Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI,original_data["ch"].split('.')[1])
            formatted_dict['ts'] = original_data['ts']
            formatted_dict['latest_price'] = ''
            formatted_dict['latest_amount'] = ''
            formatted_dict['max_buy1_price'] = ''
            formatted_dict['max_buy1_amt'] = ''
            formatted_dict['min_sell1_price'] = ''
            formatted_dict['min_sell1_amt'] = ''
            formatted_dict['pre_24h_price'] = original_data['tick']['open']
            formatted_dict['pre_24h_price_max'] = original_data['tick']['high']
            formatted_dict['pre_24h_price_min'] = original_data['tick']['low']
            formatted_dict['pre_24h_bt_finish_amt'] = original_data['tick']['amount']
            formatted_dict['pre_24h_usd_finish_amt'] = original_data['tick']['vol']
            formatted_dict["exchange"] = "huobi"
            # 返回列表，列表中的每一项为要插入数据库的数据字典记录
            formatted_data = [formatted_dict]
        elif data_type == PlatformDataType.PLATFORM_DATA_TRADE.value:
            #返回列表类型，每一项为一个字典
            symbol =  Symbol.convert_to_standard_symbol(Platform.PLATFORM_HUOBI,original_data["ch"].split('.')[1])
            write_lines = []
            tick_data = original_data['tick']['data']
            for trade in tick_data:
                formatted_dict = {}
                formatted_dict["symbol"] = symbol
                formatted_dict["id"] = str(trade['id'])
                formatted_dict["ts"] = trade['ts']
                formatted_dict["direction"] = trade['direction']
                formatted_dict["amount"] = trade['amount']
                formatted_dict["price"] = trade['price']
                formatted_dict["exchange"] = "huobi"
                write_lines.append(formatted_dict)
            # 返回列表，列表中的每一项为要插入数据库的数据字典记录
            formatted_data = write_lines


        #print(formatted_data)
        return formatted_data
