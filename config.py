#  -*- coding:utf-8 -*-
import logging

class DBConfig(object):
    RABBITMQ_HOST = "172.24.132.208"
    RABBITMQ_USERNAME = "guest"
    RABBITMQ_PWD = "guest"
    # RABBITMQ_HOST = "10.0.131.74"
    # RABBITMQ_USERNAME = "wuxiaobing"
    # RABBITMQ_PWD = "wuxiaobing"
    # mongodb服务器地址
    MONGODB_HOST = "172.24.132.208"
    # mongodb服务器端口
    MONGODB_PORT = "27017"
    # mongodb用户名
    MONGODB_USER = "data"
    # mongodb密码
    MONGODB_PWD = "data123"
    # 数据同步现货数据库名称
    MONGODB_DB_NAME = "invest"
    # okex交易所合约数据库名称
    MONGODB_DB_FUTURE = "okex_future"
    #redis配置信息
    REDIS_HOST = "10.0.131.79"
    REDIS_PORT = "6379"
    REDIS_EXPIRE_TIME = 24 * 60 * 60

    MYSQL_HOST = "localhost"
    MYSQL_PORT = "3306"
    MYSQL_USERNAME = "root"
    MYSQL_PWD = "1"
    MYSQL_DB_NAME = "invest"

    # mysql for trades account managment
    # MYSQL_ACT_HOST = '47.254.77.27'
    # MYSQL_ACT_PWD = 'data123'
    # MYSQL_ACT_DB_NAME = 'invest'
    MYSQL_ACCT_HOST = '172.24.132.191'
    MYSQL_ACCT_PORT = 3306
    MYSQL_ACCT_USERNAME = 'data'
    MYSQL_ACCT_PWD = '123.abc'
    MYSQL_ACCT_DB_NAME = 'quaninvest'
    MYSQL_ACCT_MT = 't_account'
    MYSQL_ACCT_SUBT = 't_sub_account'
    MYSQL_ACCT_SEQT = 'sequence'
    MYSQL_ACCT_EXCHANGET = 'd_exchange'
    MYSQL_ACCT_COINTYPET = 'd_coin_type'
    MYSQL_STRAREGY_tran_strategy = 't_tran_strategy'

    USD_RATE_RMB = 6.9
    # mysql for trades account managment



class TaskConfig(object):
    # 发启自动交易间隔
    TRADING_INTERVAL_SECOND = 1
    # 风险预警检测间隔
    RISK_WARNING_INTERVAL_SECOND = 1 * 24 * 60 * 60

class LogConfig(object):
    file_path = "E:\\worksplace\\quaninvest2\\logs\\"

class MathConfig(object):
    kline_precision = 18

class CryptoConfig(object):
    account_cipher_key = "PJ7TgEt2PmiUCxUlAdmEld2iCPauEy66iAoP0gB0DD4="

