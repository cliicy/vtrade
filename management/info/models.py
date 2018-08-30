#  -*- coding:utf-8 -*-
from sqlalchemy import Column, String, Table, MetaData, Integer, Numeric, DateTime, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DBConfig
import pymysql

pymysql.install_as_MySQLdb()

# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine(f'mysql+mysqlconnector://{DBConfig.MYSQL_ACCT_USERNAME}:{DBConfig.MYSQL_ACCT_PWD}@{DBConfig.MYSQL_ACCT_HOST}:{DBConfig.MYSQL_ACCT_PORT}/{DBConfig.MYSQL_ACCT_DB_NAME}')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


class Account(Base):
    # 表的名字:
    __tablename__ = DBConfig.MYSQL_ACCT_MT
    # 字段
    account_id = Column(Integer,nullable=False,primary_key=True)
    user_id = Column(Integer)
    exchange_id = Column(String(20))
    coin_to_usd = Column(Numeric(20, 4))
    coin_to_cny = Column(Numeric(20, 4))
    createtime = Column(DateTime)
    update_time = Column(DateTime)

    def __init__(self,account_id,user_id,exchange_id,coin_to_usd,coin_to_cny,createtime,update_time):
        self.account_id = account_id
        self.user_id = user_id
        self.exchange_id = exchange_id
        self.coin_to_usd = coin_to_usd
        self.coin_to_cny = coin_to_cny
        self.createtime = createtime
        self.update_time = update_time

class SubAccount(Base):
    # 表的名字:
    __tablename__ = DBConfig.MYSQL_ACCT_SUBT
    sub_account_id = Column(Integer, nullable=False, primary_key=True)
    account_id = Column(Integer, primary_key=True)
    account_type = Column(String(20))
    coin_type_id = Column(String(20))
    coin_amt = Column(Numeric(16, 10))
    future_amt = Column(Numeric(16, 10))
    createtime = Column(DateTime)

    def __init__(self,sub_account_id,account_id,account_type,coin_type_id,coin_amt,future_amt,createtime):
        self.sub_account_id = sub_account_id
        self.account_id = account_id
        self.account_type = account_type
        self.coin_type_id = coin_type_id
        self.coin_amt = coin_amt
        self.future_amt = future_amt
        self.createtime = createtime


class Exchange(Base):
    __tablename__ =    DBConfig.MYSQL_ACCT_EXCHANGET
    exchange_id = Column(String(20), primary_key=True)
    exchange_name = Column(String(30))
    e_desc = Column(String(500))
    is_enabled = Column(String(20))


class CoinType(Base):
    __tablename__ =    DBConfig.MYSQL_ACCT_COINTYPET
    coin_type_id = Column(String(20), primary_key=True)
    coin_type_name = Column(String(30))
    e_desc = Column(String(500))
    is_enabled = Column(String(20))

class T_tran_strategy(Base):
    __tablename__ =    DBConfig.MYSQL_STRAREGY_tran_strategy

    tran_strategy_id = Column(Integer, primary_key=True)
    tran_strategy_name = Column(String(300))
    e_status = Column(String(20))
    e_desc = Column(String(500))
    e_comment = Column(String(2000))
    createtime = Column(DateTime)
    create_usrer = Column(DateTime)
    update_time = Column(DateTime)
    update_user = Column(DateTime)


if __name__ == '__main__':
    pass
