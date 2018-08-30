#  -*- coding:utf-8 -*-
from sqlalchemy import Table
from management.info.models import Base
from management.info.models import engine
from management.info.models import DBSession
from management.info.models import Account
from management.info.models import SubAccount
from investment.enums import Symbol,Platform,ContractType,OKEX_SYMBOL_LIST,OKEX_FUTURE_SYMBOL_LIST
from sqlalchemy.sql import select
from config import DBConfig
from datetime import datetime
from investment.api.services import TransactionService
contract_type_list =[ContractType.THIS_WEEK,ContractType.NEXT_WEEK,ContractType.QUARTER]
#  TokenTrading 币币账户 Futures 合约账户 'Fiat_to_Token', 法币账户暂时无法通过api去查询余额
account_type = [ 'TokenTrading','Futures'] # 只有Futures才有子账户
default_usd = ['usdt']
okex_token = []
for item in OKEX_SYMBOL_LIST:
    okex_token.append(item.split('_')[0])

okex_future = []
for item in OKEX_FUTURE_SYMBOL_LIST:
    if isinstance(item,str):
        okex_future.append(item.split('_')[0])


okex_platform = Platform.PLATFORM_OKEX
okex_future_platform = Platform.PLATFORM_OKEX_FUTURE

class AccountService(object):
    """
    获取账户余额后写入mysql数据库：DB:invest tables: t_account t_sub_account
                                quaninvest tables: t_account t_sub_account
    """
    def __init__(self,exchange,coin_info):
        self._exchange = exchange # 交易所名称
        self._coins_balance_info = coin_info

    def writesubaccount(self, coin2usd_container, **kwargs):
        """
        # 写信息到子账户表中
            # get the coin type ID from table d_coin_type
        :param coin2usd_container:
        :param kwargs:
        :return:
        """
        if ('connection' in kwargs):
            _connection = kwargs['connection']
        if ('token_name' in kwargs):
            _token_name = kwargs['token_name']
        if ('trading_platform' in kwargs):
            _trading_platform = kwargs['trading_platform']
        if ('sessionmaker' in kwargs):
            _sessionmaker = kwargs['sessionmaker']
        if ('account_id' in kwargs):
            _account_id = kwargs['account_id']
        if ('coin_amt' in kwargs):
            _coin_amt = kwargs['coin_amt']
        if ('future_amt' in kwargs):
            _future_amt = kwargs['future_amt']
        if ('account_type' in kwargs):
            _account_type = kwargs['account_type']
        if ('contract_type' in kwargs):
            _contract_type = kwargs['contract_type']
        if ('symbol_get' in kwargs):
            _symbol_get = kwargs['symbol_get']
        coin_to_usd = coin2usd_container[0]  # 将要写入主账户的所有 合约账户或者币币账户 币种对应的USDT的值
        # get the value of 币种对应于USDT
        if _contract_type is None:
            trades_info = TransactionService(_trading_platform).get_ticker_info(
                symbol_get=Symbol.get_currency_pair(_trading_platform, _symbol_get),contract_type=_contract_type)
            coin_to_usd_rate = trades_info['ticker']['last']
        else:
            future_info = TransactionService(_trading_platform).get_future_index(symbol_get=Symbol.get_currency_pair(_trading_platform, _symbol_get))
            coin_to_usd_rate = future_info['future_index']

        coin_to_usd = coin_to_usd + float(_coin_amt) * float(coin_to_usd_rate)
        coin2usd_container[0] = coin_to_usd
        subacctseq = "SELECT NEXTVAL('sub_acctseq');"
        result = _connection.execute(subacctseq)
        for row in result:
            sub_account_id = row[0]
        # 获取coin_type的ID
        coin_table = Table(DBConfig.MYSQL_ACCT_COINTYPET, Base.metadata, autoload=True)
        coin_typeid_cmd = select([coin_table.c.coin_type_id]).where(
            coin_table.c.coin_type_name == _token_name)
        result = _connection.execute(coin_typeid_cmd)
        for row in result:
            coin_type_id = row[0]
        createtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subaccount = SubAccount(sub_account_id, _account_id, _account_type, coin_type_id, _coin_amt,
                                _future_amt, createtime)
        _sessionmaker.merge(subaccount)
        _sessionmaker.commit()  # 写入子账户

    def updatedb(self):
        """
        调用写入子账户函数
        写总账户
        :return:
        """
        session = DBSession()
        account_id = 0
        exchange_id = 0
        # get account_id
        with engine.connect() as conn:
            acctseq = "SELECT NEXTVAL('acctseq');"
            result = conn.execute(acctseq)
            for row in result:
                account_id = row[0]
            # get user_id
            userseq = "SELECT NEXTVAL('userseq');"
            result = conn.execute(userseq)
            for row in result:
                user_id = row[0]
            # get the exchange ID from table d_exchange
            exchange = Table(DBConfig.MYSQL_ACCT_EXCHANGET, Base.metadata, autoload=True)
            exchange_cmd = select([exchange.c.exchange_id]).where(exchange.c.exchange_name == self._exchange)
            result = conn.execute(exchange_cmd)
            for row in result:
                exchange_id = row[0]
            # do test: get balance of fcoin's account
            coin_to_cny = 0 # 人民币预估值
            coin_to_usd = [0] # 将要写入主账户的所有 合约账户或者币币账户 币种对应的USDT的值
            # okex有合约账户、币币账户。 合约账户里有分多种不同的合约类型
            if okex_platform.value in self._exchange:
                # 获取币币账户的余额信息
                rdata = self._coins_balance_info['token_account']
                for key,value in rdata['funds']['free'].items():
                    if key == default_usd[0]:
                        coin_to_usd[0] = coin_to_usd[0]+float(value)
                    if key in okex_token:
                        symbol_get = '{0}_{1}'.format(key, 'usdt')
                        self.writesubaccount(coin_to_usd,token_name=key,coin_amt=value,contract_type=None,
                                        trading_platform=okex_platform,future_amt=0,account_id=account_id,
                                        account_type=account_type[0],symbol_get=symbol_get,sessionmaker=session,connection=conn)
                usd2rmb_rate = TransactionService(okex_platform).get_exchange_rate()
                coin_to_cny = coin_to_cny + coin_to_usd[0] * float(usd2rmb_rate['rate'])  # usd 对应的 人民币数值
                # 获取合约账户的余额信息
                futuredata = self._coins_balance_info['future_account']
                for type in contract_type_list:
                    for key, value in futuredata.items():
                        if key == default_usd[0]:
                            coin_to_usd[0] = coin_to_usd[0]+float(value)
                        if key in okex_future:
                            coin_amt = value['keep_deposit']  # 保证金
                            future_amt = value['account_rights']  # 账户权益,持有币的总个数
                            symbol_get = '{0}_{1}'.format(key, 'usd')
                            self.writesubaccount(coin_to_usd, token_name=key, coin_amt=coin_amt,contract_type=type,
                                                trading_platform=okex_future_platform,account_id=account_id,
                                                 future_amt=future_amt, account_type=account_type[1],symbol_get=symbol_get,
                                                 sessionmaker=session,connection=conn)
                # 写余额信息到主账户
                usd2rmb_rate = TransactionService(okex_future_platform).get_exchange_rate()
                coin_to_cny = coin_to_cny + coin_to_usd[0] * float(usd2rmb_rate['rate']) # usd 对应的 人民币数值
                createtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                update_time = createtime
                acfcoin = Account(account_id, user_id, exchange_id, coin_to_usd[0], coin_to_cny, createtime, update_time)
                session.merge(acfcoin)
                session.commit()


if __name__ == '__main__':
    # test for save balance to mysqldb
    # calculate balance of fcoin
    # coins_balance = TransactionService(Platform.PLATFORM_FCOIN).get_account_info()
    # AccountService(Platform.PLATFORM_FCOIN.value,coins_balance,'TokenTrading').updatedb()
    # calculate balance of okex' future account
    tokent_account_info = TransactionService(Platform.PLATFORM_OKEX).get_account_info()
    future_account_info = TransactionService(Platform.PLATFORM_OKEX_FUTURE).get_account_info()
    AccountService(Platform.PLATFORM_OKEX.value, {'token_account':tokent_account_info['info'],'future_account':future_account_info['info']}).updatedb()

    print('done')
    # test for save balance of okex' future account to mysqldb
