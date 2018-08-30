#  -*- coding:utf-8 -*-
from investment.enums import PlatformDataType
from investment.enums import Platform
from investment.enums import Symbol


class FcoinDataConverter:
    """
    Fcoin数据转换器
    """

    @staticmethod
    def convert(data_type, original_data):
        """
        原始数据转化成统一格式的数据
        :param PlatformDataType: 数据类型
        :param original_data: 原始数据
        :return:统一格式的数据
        """
        # print('aaa ',original_data)
        # original_data = eval(original_data)
        original_data = eval(original_data)
        assert type(original_data) == dict
        sym = Symbol.convert_to_standard_symbol(Platform.PLATFORM_FCOIN, original_data['symbol'])
        exchange = 'fcoin'
        if 'exchange' in original_data:
            exchange = original_data['exchange']
        # print('original 类型：{0} 数据:{1} '.format(data_type,original_data))
        # 统一格式数据
        formatted_data = ""
        if data_type == PlatformDataType.PLATFORM_DATA_KLINE.value:
            # TODO kline数据转化..
            print(formatted_data)
            formatted_data = [{'symbol':sym, 'ts':original_data['ts'], 'tm_intv':original_data['tm_intv'],
                              'id':original_data['id'], 'open':original_data['open'], 'close':original_data['close'],
                              'low':original_data['low'], 'high':original_data['high'], 'amount':original_data['quote_vol'],
                              'vol':original_data['base_vol'], 'count':original_data['count'], 'exchange':exchange}]
        elif data_type == PlatformDataType.PLATFORM_DATA_DEPTH.value:
            # TODO depth数据转化..
            formatted_data = []
            print(formatted_data)
            bidlists = original_data['bids']
            asklists = original_data['asks']
            idp = 0
            nask = len(bidlists)
            while idp < nask:
                blst = bidlists[idp:idp + 2]
                alst = asklists[idp:idp + 2]
                idepth = 1 + idp / 2
                idp += 2
                formatted_data.append({'symbol':sym, 'ts':original_data['ts'], 'depth':idepth,
                                  'sell_price':alst[0], 'buy_price':blst[0], 'sell_amt':alst[1], 'buy_amt':blst[1], 'exchange':exchange})
            print(formatted_data)

        elif data_type == PlatformDataType.PLATFORM_DATA_TICKER.value:
            # TODO ticker数据转化..
            print(formatted_data)
            tdata = original_data['ticker']
            formatted_data = [{'symbol':sym, 'ts':original_data['ts'], 'latest_price':tdata[0],
                              'latest_amount':tdata[1], 'max_buy1_price':tdata[2], 'max_buy1_amt':tdata[3],
                              'min_sell1_price':tdata[4], 'min_sell1_amt':tdata[5], 'pre_24h_price':tdata[6],
                              'pre_24h_price_max':tdata[7], 'pre_24h_price_min':tdata[8], 'pre_24h_bt_finish_amt':tdata[9],
                              'pre_24h_usd_finish_amt':tdata[10], 'exchange':exchange}]
            print(formatted_data)
        elif data_type == PlatformDataType.PLATFORM_DATA_TRADE.value:
            print(formatted_data)
            # TODO trade数据转化..
            formatted_data = [{'symbol':sym, 'id':original_data['id'], 'ts':original_data['ts'],
                              'direction':original_data['side'], 'amount':original_data['amount'], 'price':original_data['price'], 'exchange':exchange}]
        print(formatted_data)
        return formatted_data
