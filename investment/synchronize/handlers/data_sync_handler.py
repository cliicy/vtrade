#  -*- coding:utf-8 -*-
from config import DBConfig as Config , MathConfig
from investment.enums import Platform, PlatformDataType, PlatformDataTypeIndex
from investment.synchronize.handlers.converter import *
from investment.synchronize.handlers.mq_receiver import MqReceiver
from pymongo import MongoClient
import operator as op
import redis
from decimal import Decimal, getcontext


class DataSyncHandler:
    """
    数据同步器
    """
    # 平台类型
    platform = ""
    # 数据类型
    platform_data_type = ""
    db_type = ""
    # 统一格式数据
    formatted_data = []
    # redis
    _redis = None
    redis_db = []

    def __init__(self, platform, platform_data_type, db_type):
        """
        初始化数据同步器
        :param platform: 平台
        :param platform_data_type: 数据类型
        """
        self.platform = platform
        self.platform_data_type = platform_data_type
        self.db_type = db_type
        mongo_url = 'mongodb://' + Config.MONGODB_USER + \
                    ':' + Config.MONGODB_PWD + '@' + Config.MONGODB_HOST + ':' + \
                    Config.MONGODB_PORT + '/' + Config.MONGODB_DB_NAME
        self.client = MongoClient(mongo_url)
        self.db = self.client.get_database()
        self.db_future = self.client[Config.MONGODB_DB_FUTURE]
        # 初始化redis
        pool = redis.ConnectionPool(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
        self._redis = redis.StrictRedis(connection_pool=pool)
        # 初始化redis db 1～20
        for i in range(0, 21, 1):
            self.redis_db.append(redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=i))

    def sync(self, original_data):
        """
        数据同步
        :param original_data: 原始数据
        :return:
        """

        if self.platform == Platform.PLATFORM_BINANCE.value:
            self.formatted_data = BinanceDataConverter.convert(self.platform_data_type, original_data)
        elif self.platform == Platform.PLATFORM_FCOIN.value:
            self.formatted_data = FcoinDataConverter.convert(self.platform_data_type, original_data)
        elif self.platform == Platform.PLATFORM_HUOBI.value:
            self.formatted_data = HuobiDataConverter.convert(self.platform_data_type, original_data)
        elif self.platform == Platform.PLATFORM_OKCOIN.value:
            self.formatted_data = OkcoinDataConverter.convert(self.platform_data_type, original_data)
        elif self.platform == Platform.PLATFORM_OKCOIN_FUTURE.value:
            self.formatted_data = OkcoinFutureDataConverter.convert(self.platform_data_type, original_data)
        print("sync_mongo:", self.formatted_data)
        self.save_mongo(self.formatted_data)

    def sync_redis(self, original_data):
        """
        数据同步
        :param original_data: 原始数据
        :return:
        """

        if self.platform == Platform.PLATFORM_BINANCE.value:
            self.formatted_data = BinanceDataConverter.convert(self.platform_data_type, original_data)
        elif self.platform == Platform.PLATFORM_FCOIN.value:
            self.formatted_data = FcoinDataConverter.convert(self.platform_data_type, original_data)
        elif self.platform == Platform.PLATFORM_HUOBI.value:
            self.formatted_data = HuobiDataConverter.convert(self.platform_data_type, original_data)
        elif self.platform == Platform.PLATFORM_OKEX.value:
            self.formatted_data = OkcoinDataConverter.convert(self.platform_data_type, original_data)
        elif self.platform == Platform.PLATFORM_OKEX_FUTURE.value:
            self.formatted_data = OkcoinFutureDataConverter.convert(self.platform_data_type, original_data)
        print("sync_redis:", self.formatted_data)
        self.save_redis(self.formatted_data)

    def save_mongo(self, data):
        """
        保存到mongodb
        :param data:数据
        :return:
        """
        try:
            collection = self.platform_data_type
            # 不同的数据类型对应数据库中不同的collection，不同的数据类型，去重逻辑不同

            # 如果是平台类型是okex的合约数据，则向合约数据库写入数据
            if op.eq(self.platform, Platform.PLATFORM_OKCOIN_FUTURE.value):
                col = self.db_future[collection]
                # 如果是kline数据，对传入的数据中的id 和 exchange symbol contractType字段进行查找，有则跟新，没有则插入
                if op.eq(collection, PlatformDataType.PLATFORM_DATA_KLINE.value):
                    for msg in data:
                        qurry_dict = {"symbol": msg["symbol"], "contractType": msg["contractType"], "id": msg["id"],
                                      "exchange": msg["exchange"]}
                        # 新增修改mongo
                        if (col.find(qurry_dict).count()) > 0:
                            col.update_many(qurry_dict, {'$set': msg})
                        else:
                            col.insert_one(msg)
                # 如果是trade，ticker，depth 类型数据，对待插入数据的所有的项进行查询，如果有则跳过，没有则插入
                if collection in [PlatformDataType.PLATFORM_DATA_DEPTH.value,
                                  PlatformDataType.PLATFORM_DATA_TICKER.value,
                                  PlatformDataType.PLATFORM_DATA_TRADE.value]:
                    for msg in data:
                        # 新增mongo
                        qurry_dict = msg
                        if (col.find(qurry_dict).count()) > 0:
                            continue
                        else:
                            col.insert_one(msg)

            # 其他四个交易所现货数据入库处理
            else:
                col = self.db[collection]
                # 如果是现货kline数据，对传入的数据中的id 和 exchange symbol字段进行查找，有则跟新，没有则插入
                if op.eq(collection, PlatformDataType.PLATFORM_DATA_KLINE.value):
                    for msg in data:
                        qurry_dict = {"symbol": msg["symbol"], "id": msg["id"], "exchange": msg["exchange"]}
                        if (col.find(qurry_dict).count()) > 0:
                            col.update_many(qurry_dict, {'$set': msg})
                        else:
                            col.insert_one(msg)
                # 如果是trade，ticker，depth 类型数据，对待插入数据的所有的项进行查询，如果有则跳过，没有则插入
                if collection in [PlatformDataType.PLATFORM_DATA_DEPTH.value,
                                  PlatformDataType.PLATFORM_DATA_TICKER.value,
                                  PlatformDataType.PLATFORM_DATA_TRADE.value]:
                    for msg in data:
                        qurry_dict = msg
                        if (col.find(qurry_dict).count()) > 0:
                            continue
                        else:
                            col.insert_one(msg)
        except Exception as e:
            print(str(e))

    def save_redis(self, data):
        """
        保存到redis
        :param data:数据
        :return:
        """
        # 获得redis数据连接
        index = PlatformDataTypeIndex.getIndex(self.platform, self.platform_data_type)
        self._redis = self.redis_db[index]
        try:
            collection = self.platform_data_type
            # 不同的数据类型对应数据库中不同的collection，不同的数据类型，去重逻辑不同

            # 如果是现货kline数据，对传入的数据中的id 和 exchange symbol字段进行查找，有则跟新，没有则插入
            if op.eq(collection, PlatformDataType.PLATFORM_DATA_KLINE.value):
                for msg in data:
                    # 新增修改redis
                    # s = self._redis.set(f'{msg["symbol"]}.{str(msg["id"])}.{msg["contractType"]}', msg,
                    #                     ex=Config.REDIS_EXPIRE_TIME)
                    # print(s)
                    self.save_kline(msg)
            # 如果是trade，ticker，depth 类型数据，对待插入数据的所有的项进行查询，如果有则跳过，没有则插入
            if collection in [PlatformDataType.PLATFORM_DATA_DEPTH.value,
                              PlatformDataType.PLATFORM_DATA_TICKER.value,
                              PlatformDataType.PLATFORM_DATA_TRADE.value]:
                for msg in data:
                    # 新增redis
                    s = self._redis.setex(f'{msg["symbol"]}.{str(msg["id"])}.{msg["contractType"]}', Config.REDIS_EXPIRE_TIME, msg
                                          )
                    print(s)
        except Exception as e:
            print(str(e))

    def start(self):
        """
        数据同步启动
        :return:
        """
        if (self.db_type == "redis"):
            # 同步redis
            MqReceiver(self.platform, self.platform_data_type).receive(self.sync_redis, topic="_r")
        elif (self.db_type == "mongo"):
            MqReceiver(self.platform, self.platform_data_type).receive(self.sync)

    def save_kline(self, msg):
        dic_name = f'{msg["exchange"]}.{msg["symbol"]}.{str(msg["id"])}'
        if (msg["contractType"]) == "this_week":
            dic = {"symbol_x": msg["symbol"], "contractType_x": msg["contractType"], "id": msg["ts"],
                   "open_x": msg["open"], "close_x": msg["close"], "vol_x": msg["vol"], "count_x": round(msg["count"])}
        elif (msg["contractType"]) == "next_week":
            dic = {"symbol_y": msg["symbol"], "contractType_y": msg["contractType"], "id": msg["ts"],
                   "open_y": msg["open"], "close_y": msg["close"], "vol_y": msg["vol"], "count_y": round(msg["count"])}
        elif (msg["contractType"]) == "quarter":
            dic = {"symbol": msg["symbol"], "contractType": msg["contractType"], "id": msg["ts"],
                   "open": msg["open"], "close": msg["close"], "vol": msg["vol"], "count": round(msg["count"])}
        s = self._redis.hmset(dic_name, dic)
        hash = self._redis.hgetall(dic_name)
        # hash1 = self._redis.dump(dic_name)
        print("hash=", hash)
        minus_close = None
        minus_open = None
        fee = None
        getcontext().prec = MathConfig.kline_precision
        if b"close_x" in hash and b"close_y" in hash and b"close" in hash:
            minus_close = Decimal(2) * Decimal(hash[b"close_y"].decode()) - Decimal(hash[b"close"].decode()) - Decimal(
                hash[b"close_x"].decode())
        if b"open_x" in hash and b"open_y" in hash and b"open" in hash:
            minus_open = Decimal(2) * Decimal(hash[b"open_y"].decode()) - Decimal(hash[b"open"].decode()) - Decimal(
                hash[b"open_x"].decode())
        if b"close_x" in hash and b"close_y" in hash and b"close" in hash:
            fee = (Decimal(2) * Decimal(hash[b"close_y"].decode()).quantize(Decimal('0.000')) - Decimal(
                hash[b"close"].decode()) - (Decimal(hash[b"close_x"].decode())).quantize(Decimal('0.000'))) * Decimal(
                0.001)
        calc_dic = {"minus_close": minus_close, "minus_open": minus_open, "fee": fee}
        print("calc_dic=", calc_dic)
        s = self._redis.hmset(dic_name, calc_dic)


if __name__ == '__main__':
    # DataSyncHandler(Platform.PLATFORM_BINANCE.value, PlatformDataType.PLATFORM_DATA_KLINE.value, "mongo").start()
    # DataSyncHandler(Platform.PLATFORM_OKEX_FUTURE.value, PlatformDataType.PLATFORM_DATA_KLINE.value, "redis").start()
    DataSyncHandler(Platform.PLATFORM_OKEX_FUTURE.value, PlatformDataType.PLATFORM_DATA_TRADE.value, "redis").start()
    # msg = eval("{'symbol': 'EOS/USDT', 'ts': 1535013120000, 'tm_intv': '1m', 'id': 1535013120000, 'open': 4.627, 'close': 4.624, 'low': 4.624, 'high': 4.628, 'amount': '', 'vol': 9683.263533683334, 'count': 4480, 'contractType': 'quarter', 'exchange': 'okex_future'}")
    # DataSyncHandler(Platform.PLATFORM_OKEX_FUTURE.value, PlatformDataType.PLATFORM_DATA_KLINE.value, "redis").kline_parse(msg)
