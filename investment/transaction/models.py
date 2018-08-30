#  -*- coding:utf-8 -*-
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DBConfig
import pymysql
import datetime


pymysql.install_as_MySQLdb()

# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine(f'mysql://{DBConfig.MYSQL_ACCT_USERNAME}:{DBConfig.MYSQL_ACCT_PWD}@{DBConfig.MYSQL_ACCT_HOST}:{DBConfig.MYSQL_ACCT_PORT}/{DBConfig.MYSQL_ACCT_DB_NAME}')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


class Trans(Base):
    """
    交易model类
    """
    # 表的名字:
    __tablename__ = 't_trans'
    # 字段
    trans_id = Column(Integer, primary_key = True, autoincrement=True)
    trans_inst_id = Column(Integer) # 策略实例_id
    ex_trans_id = Column(String(100)) # 交易所交易id
    user_id = Column(Integer)
    trans_type = Column(String(20)) # 挂单类型 开仓 0；平仓 1；爆仓 2
    tran_strategy_id = Column(Integer)
    amt_left = Column(Numeric(20, 4))
    e_status = Column(String(20))
    create_time = Column(DateTime)
    trans_amt = Column(Numeric(20, 4))
    trans_price = Column(Numeric(20, 4))
    deal_amt = Column(Numeric(16, 10))
    deal_price = Column(Numeric(20, 4))
    symbol = Column(String(500))
    fee = Column(Numeric(20, 4))
    update_time = Column(DateTime)
    contract_type = Column(String(20))
    account_id = Column(Integer)
    trans_time = Column(DateTime)

    def save(trans):
        """
        新加/修改交易表
        :param trans:
        :return:
        """
        # 创建session对象:
        session = DBSession()
        # 添加到session:
        session.merge(trans)
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()

    def select(self, **kwargs):
        """
        新加/修改交易表
        :param trans:
        :return:
        """
        # 创建session对象:
        session = DBSession()
        filterList = []
        # 将参数找到如果有则赋值
        if("trans_id" in kwargs):
            _trans_id = kwargs["trans_id"]
            filterList.append(Trans.contract_type == _trans_id)
        if("ex_trans_ids" in kwargs):
            _ex_trans_ids = f'({kwargs["ex_trans_ids"]})'
            filterList.append(Trans.ex_trans_id in _ex_trans_ids)
        if("contract_type" in kwargs):
            _contract_type = kwargs["contract_type"]
            filterList.append(Trans.contract_type == _contract_type)
        # 查询:
        # print(_trans_id)
        filters = tuple(filterList)
        select = session.query(Trans).filter(*filters).all()
        # print(select)
        # 关闭session:
        session.close()
        # 返回查询结果
        return select

class Trans_inst(Base):
    """
    策略实例model类
    """
    # 表的名字:
    __tablename__ = 't_trans_inst'
    # 字段
    user_id = Column(Integer, primary_key=True)
    trans_inst_id = Column(Integer, primary_key=True,autoincrement=True)
    tran_strategy_id = Column(Integer, primary_key=True)
    is_positive = Column(Boolean)
    is_simulate = Column(Boolean)
    start_tm = Column(DateTime)
    open_amt_limit = Column(Numeric(20, 4))
    close_amt_limit = Column(Numeric(20, 4))
    e_status = Column(String(20))
    create_time = Column(DateTime)
    symbol = Column(String(20))
    exchange_ids = Column(String(20))

    def save(trans_inst):
        """
        新加/修改策略实例表
        :param trans:
        :return:
        """
        # 创建session对象:
        session = DBSession()
        # 添加到session:
        session.merge(trans_inst)
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()
    def select(self,**kwargs):
        """
        新加/修改交易表
        :param trans:
        :return:
        """
        # 创建session对象:
        session = DBSession()
        # 将参数找到如果有则赋值
        if("user_id" in kwargs):
            _user_id = kwargs["user_id"]
        # 查询:
        # print(_user_id)
        select = session.query(Trans_inst).filter(Trans_inst.user_id == _user_id).first()
        print(select)
        # 关闭session:
        session.close()
        # 返回查询结果
        return select

class T_trans_detail(Base):
    """
    交易model类
    """
    # 表的名字:
    __tablename__ = 't_trans_detail'
    # 字段
    trans_sq = Column(String(100), primary_key = True)
    trans_id = Column(Integer)
    user_id = Column(Integer)
    account_id = Column(Integer)
    trans_time = Column(DateTime)
    trans_amt = Column(Numeric(20, 4))
    trans_price = Column(Numeric(20, 4))
    coin_amt = Column(Numeric(16, 10))
    fee = Column(Numeric(20, 4))
    symbol = Column(String(20))
    exchange_id = Column(String(20))
    trans_status = Column(String(20))

    def save(t_trans_detail):
        """
        新加/修改交易表
        :param trans:
        :return:
        """
        # 创建session对象:
        session = DBSession()
        # 添加到session:
        session.merge(t_trans_detail)
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()
    def select(self,**kwargs):
        """
        新加/修改交易表
        :param trans:
        :return:
        """
        # 创建session对象:
        session = DBSession()
        # 将参数找到如果有则赋值
        if("trans_sq" in kwargs):
            _trans_sq = kwargs["trans_sq"]
        # 查询:
        # print(_trans_sq)
        select = session.query(T_trans_detail).filter(T_trans_detail.trans_sq == _trans_sq).first()
        print(select)
        # 关闭session:
        session.close()
        # 返回查询结果
        return select

if __name__ == '__main__':
    Trans_inst(user_id=1,
               tran_strategy_id=1,
               is_positive=True,
               is_simulate=True,
               start_tm= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               open_amt_limit=20.44,
               close_amt_limit=20.44,
               e_status = '1',
               create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               symbol='btc_usd',
               exchange_ids='btc_usdadad1111').save()
    # Trans(
    #       trans_inst_id=22222,
    #       ex_trans_id='usdt_aaaaaa',
    #       user_id=22222,
    #       trans_type='usdt_aaaaaa',
    #       tran_strategy_id=22222,
    #       amt_left=12.1,
    #       e_status='usdt_aaaaaa',
    #       create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #       trans_amt=12.1,
    #       trans_price=12.1,
    #       deal_amt=12.1,
    #       deal_price=12.1,
    #       symbol='12.1',
    #       fee=12.1,
    #       update_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #       contract_type='usdt_aaaaaa',
    #       account_id=22222,
    #       trans_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).save()
    # T_trans_detail(trans_sq='asdasd',
    #                trans_id=11111111,
    #                user_id=11111111,
    #                account_id=11111111,
    #                trans_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #                trans_amt=222.333,
    #                trans_price=222.333,
    #                coin_amt=222.666,
    #                fee=222.333,
    #                symbol='btc_usd',
    #                exchange_id='btc_usd',
    #        s        trans_status='btc_usd'
    #                ).save()
    # Trans().select(trans_id=1)
    # Trans_inst().select(user_id=1)
    # T_trans_detail().select(trans_sq='asdasd')