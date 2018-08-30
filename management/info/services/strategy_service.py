#  -*- coding:utf-8 -*-
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DBConfig
import pymysql
import datetime
from config import DBConfig
from management.info.models import T_tran_strategy
pymysql.install_as_MySQLdb()

# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine(f'mysql+mysqlconnector://{DBConfig.MYSQL_ACCT_USERNAME}:{DBConfig.MYSQL_ACCT_PWD}@{DBConfig.MYSQL_ACCT_HOST}:{DBConfig.MYSQL_ACCT_PORT}/{DBConfig.MYSQL_ACCT_DB_NAME}')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

class StrategyService(object):

    def select(self,**kwargs):
        """
        新加/修改交易表
        :param trans:
        :return:
        """
        # 创建session对象:
        session = DBSession()
        select = session.query(T_tran_strategy).all()
        print(select)
        # 关闭session:
        session.close()
        # 返回查询结果
        return select

if __name__ == '__main__':
    S = StrategyService()
    S.select()