#  -*- coding:utf-8 -*-
import math,sys,time

from quaninvest.investment.enums import *
from quaninvest.investment.api.services import *

class TradingStraregyHandler:
    """
    交易策略判定主程序
    """

    # 最多重复请求数据次数
    qurry_data_max = 3

    #有效数据条数
    data_num = 58
    #策略窗口值
    window_num = 60
    #最大最小值均值个数设定
    topn = 5


    def check_contract_data(self,left_leg,mid,right_leg):
        """
            获取三个合约的数据并对其进行数据有效性检测和处理
            有效数据返回 true 和 共有的时间戳数据
            无效数据返回 false 和 空列表【】
        """
        left_leg = left_leg
        mid = mid
        right_leg = right_leg

        #当前时间的分钟 0秒 计算 13位的unix时间戳，作为检测标准 检测三个合约kline数据的最后一条数据kline id
        now = int(time.time())
        timeArray = time.localtime(now)
        #print(timeArray)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
        a = time.strptime(otherStyleTime, "%Y-%m-%d %H:%M")

        latest_kline_id = int(time.mktime(a)) * 1000
        print(latest_kline_id)

        #合约最后一条数据kline id 检测

        if right_leg[-1][0] != latest_kline_id or mid[-1][0] != latest_kline_id or left_leg[-1][0] != latest_kline_id:
            print("实时kline数据缺失，重新请求")
            return  False,[]

        right_ts=[v[0] for v in right_leg]
        left_ts =[v[0] for v in left_leg]
        mid_ts =[v[0] for v in mid]

        #时间戳取交集
        intersection_ts = set(set(right_ts).intersection(set(left_ts))).intersection(set(mid_ts))

        intersection_num = len(intersection_ts)
        if intersection_num < self.data_num:
            print("获取数据质量差，重新请求")
            return False,[]
        #三个合约的时间戳交集
        else:
            kline_ids = sorted(list(intersection_ts))
            return True,kline_ids


    def check_straregy(self):
        """
          交易策略执行之前的交易条件审查，如果满足条件 check_status 设置为True，才能执行交易策略程序

           策略检查项目
             1.不交易时间控制
                 周五15:50~17:00
             2.账户异常不交易
                 账户被封禁
             3.账户余额异常不交易
                 币种持仓折合合约小于4张
             4.止盈控制
             5.止损控制
             6.模拟交易控制
                 判断策略，记录策略实例
                 不开仓
             7.交易所开关控制
             8.币种开关控制
             9.策略运行开关控制
             10.策略运行起止时间控制

           【待实现】
         """
        return True


    def check_close_order(self):
        """
        检查是否有未完成的平仓
        【待实现】
        :return:
             True 有未完成的平仓
             False 没有有未完成的平仓
        """
        return False


    def check_open_order(self):
        """
        检查是否有未完成的开仓
        【待实现】
        :return:
             True 有未完成的开仓
             False 没有有未完成的开仓
        """
        return False


    def explosion_op(self):
        """
         爆仓功能
        【待实现】
        :return:
        """
        pass


    def close_op(self):
        """
        平仓功能
        【待实现】
        :return:
        """
        pass



    def supplent_op(self):
        """
        补单功能
        【待实现】
        :return:
        """
        pass


    def reorder_op(self):

        """
        重新下单功能
        【待实现】
        :return:
        """
        pass


    def get_strategy_satus(self,strategy_id):
        """
        获取策略实例id的策略方向和策略状态
        从数据库表中取对应字段
        【待实现】
        :return:
             策略实例的状态
             策略实例的方向（正向还是反向）
        """

        #用什么值来代表不同的方向 和 不同的状态？【待确定】
        direction = 0 #正向
        status = 0#
        return direction,status

    #默认left_leg为本周合约  mid 为下周合约  right_leg为季度合约
    def butterfly_trade(self, symbol,left_leg = ContractType.THIS_WEEK,mid = ContractType.NEXT_WEEK,right_leg = ContractType.QUARTER):

        # 策略是否可以执行标志
        check_status = False
        # 策略执行检查
        check_status = self.check_straregy()
        left_leg = left_leg
        mid = mid
        right_leg = right_leg

        if check_status:

            #先检查是否有未完成的平仓
            if self.check_close_order():
                #有的话走重新下单的平仓处理分支
                self.reorder_op()
            #没有的话走策略机会判断逻辑
            else:
                #期货历史数据列表【方法待确定】
                right_kline = []
                left_kline = []
                mid_kline = []
                #数据有效性标志
                data_ok = False

                i = 0
                #最多请求3次数据，如果数据都无效则不执行
                while not data_ok and i < self.qurry_data_max:
                    #调用请求数据方法
                    kline_dict = RealTimeInquiry("okex_future").get_kline_info(symbol_get=symbol)
                    left_kline = kline_dict[left_leg]
                    mid_kline = kline_dict[mid]
                    right_kline = kline_dict[right_leg]
                    #数据有效性判断
                    data_ok,kline_ids = self.check_contract_data(left_kline,mid_kline,right_kline)

                    print(data_ok,kline_ids)
                    i += 1

                # 三个合约取出共有的时间戳交易数据作为策略计算的有效数据
                if data_ok:
                    right_kline_clear = [v for v in right_kline if v[0] in kline_ids]
                    left_kline_clear = [v for v in left_kline if v[0] in kline_ids]
                    mid_kline_clear = [v for v in mid_kline if v[0] in kline_ids]

                    # 期货交易货币
                    symbol = symbol
                    # 窗口大小
                    window_num = self.window_num
                    # topn
                    topn = self.topn



                    # （3）合约账户持仓币的个数和合约持仓 【待获取】
                    coin_num, contract_num = self.get_account_coin_contract(symbol)

                    # （4）套利机会计算

                    # 价差计算结果列表
                    minus_close = []



                    for index in range(len(kline_ids)):
                        minus_close.append(2 * mid_kline_clear[index][4] - right_kline_clear[index][4] - left_kline_clear[index][4])

                    sort_list = sorted(minus_close[0:-1])
                    # 最大的几个价格
                    max_list = sort_list[0 - topn:]
                    # 最小的几个价格
                    min_list = sort_list[0:topn]
                    max_mean = self.get_average(max_list)
                    min_mean = self.get_average(min_list)

                    # （5）计算资金容量对应最大的可套利张数lot

                    # 货币实时价格（美元）【待获取】
                    coin_price = 0
                    # 合约每张的价格 单位为美元
                    per_price = 10
                    if Symbol.BTC_USDT == symbol:
                        per_price = 100

                    # 持仓对应张数H 10为杠杆倍数
                    H = math.floor(10 * coin_num * coin_price / per_price / 4)

                    # 实时本周、次周/2、季度三者交易量的最小值乘以10%
                    account_limit = min(left_kline_clear[-1][5],mid_kline_clear[-1][5]/2,right_kline_clear[-1][5]) * 0.1

                    # 资金容量对应最大的可套利张数，按照为单位下单
                    lot = min(account_limit, H)

                    # （6）实时行情的基差
                    diff = minus_close[-1]

                    # (7)判断套利机会
                    # 成本值 实时行情的（2倍mid收盘价 + left_leg收盘价 + right_leg收盘价） / 1000
                    cost_raw = (2 * mid_kline_clear[-1][4]  + left_kline_clear[-1][4] + right_kline_clear[-1][4])* 0.001
                    # 手续费 实时行情的（2倍mid收盘价 + left_leg收盘价 + right_leg收盘价） / 1000
                    cost_fee = cost_raw

                    # 获取交易实例的数据库状态 策略方向和策略状态
                    is_positive, e_status = self.get_strategy_satus(strategy_id=0)

                    #正向开仓/反向平仓条件判断
                    if diff > max_mean and (max_mean - min_mean - cost_raw) > cost_fee:


                        #如果状态为正向开仓已完成
                        if is_positive == "正向" and e_status == "开仓已完成":
                            #允许重复开仓逻辑
                            pass

                        #如果状态为正向开仓（部分完成未完成），重新下单（追单）
                        elif is_positive == "正向" and e_status == "开仓部分完成或开仓未进行":

                            #重新下单（追单）
                            self.reorder_op()

                        #如果有反向开仓已完成 执行反向平仓
                        elif is_positive == "反向" and e_status == "开仓已完成":
                            #反向平仓操作
                            pass
                        # 如果有反向开仓部分完成，撤单，反向平仓
                        elif is_positive == "反向" and e_status == "开仓部分完成":

                            #撤单

                            #反向平仓
                            pass

                        # 如果有反向开仓未进行，撤单，正向开仓
                        elif is_positive == "反向" and e_status == "开仓未进行":

                            #撤单

                            #正向开仓
                            pass

                        else:
                            #正向开仓
                            pass

                    #反向开仓/正向平仓条件判断
                    elif diff < min_mean and (max_mean - min_mean) > cost_fee:

                        # 如果状态为反向开仓已完成
                        if is_positive == "反向" and e_status == "开仓已完成":
                            #允许重复开仓逻辑
                            pass

                        # 如果状态为反向开仓（部分完成未完成），重新下单
                        elif is_positive == "反向" and e_status == "开仓部分完成或开仓未进行":

                            # 重新下单（追单）
                            self.reorder_op()

                        # 如果有正向开仓已完成 执行正向平仓
                        elif is_positive == "正向" and e_status == "开仓已完成":
                            # 正向平仓操作
                            pass
                        # 如果有正向开仓部分完成，撤单，正向平仓
                        elif is_positive == "正向" and e_status == "开仓部分完成":

                            # 撤单

                            # 正向平仓
                            pass

                        # 如果有正向开仓未进行，撤单，反向开仓
                        elif is_positive == "正向" and e_status == "开仓未进行":

                            # 撤单

                            # 反向开仓
                            pass

                        else:
                            # 反向开仓
                            pass

                    else:
                        #查看是否有未完成的开仓,如果有重新下单
                        if self.check_open_order():
                            self.reorder_op()

                        else:
                            pass


    def get_average(num_list):
        """
        数字列表平均数计算
        :return: 数据的平均值
        """
        sum = 0
        for i in num_list:
            sum += i
        return sum / len(num_list)


if __name__ == '__main__':

    a = TradingStraregyHandler()
    a.butterfly_trade(Symbol.EOS_USDT)


