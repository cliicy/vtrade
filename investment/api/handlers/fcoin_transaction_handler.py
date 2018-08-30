#  -*- coding:utf-8 -*-
from investment.api.handlers.transaction_handler import TransactionHandler
import investment.api.setting as config
from collections import defaultdict
from investment.api.communicators import HttpCommunicator as httpcom
from investment.enums import STANDARD_SYMBOL_LIST
from investment.enums import Symbol
from investment.enums import Platform
# from investment.api.services import UpdateRecords
import base64
import logging
import time
import hmac
import hashlib
import math
SYMBOL = [ 'BTC','USDT','XRP','BCH','ETH','LTC']


class FcoinTransactionHandler(TransactionHandler):
    """
    fcoin处理交易的通信控制器
    """
    def __init__(self):
        self.key = ''
        self.secret = ''
        self.auth(config.fcoin_setting['key'], config.fcoin_setting['secret'])
        self._balance = {}
        self._init_log()
        self.order_id = []
        self.order_list = []
        self.filled_buy_order_list = []
        self._syms = [] # 要下单得货币对列表

    def auth(self, key, secret):
        self.key = bytes(key, 'utf-8')
        self.secret = bytes(secret, 'utf-8')


    def digits(self, num, digit):
        site = pow(10, digit)
        tmp = num * site
        tmp = math.floor(tmp) / site
        return tmp

    def get_balance(self):
        """get user balance"""
        return self.signed_request('GET', 'accounts/balance')

    def get_signed(self, sig_str):
        """signed params use sha512"""
        sig_str = base64.b64encode(sig_str)
        signature = base64.b64encode(hmac.new(self.secret, sig_str, digestmod=hashlib.sha1).digest())
        return signature

    def buy(self, symbol, price, amount):
        """buy someting"""
        return self.create_order(symbol=symbol, side='buy', type='limit', price=str(price), amount=amount)

    def create_order(self, **payload):
        """create order"""
        return self.signed_request('POST', 'orders', **payload)

    def sell(self, symbol, price, amount):
        """sell someting"""
        return self.create_order(symbol=symbol, side='sell', type='limit', price=str(price), amount=amount)

    def signed_request(self, method, api_url, **payload):
        """request a signed url"""
        param=''
        if payload:
            sort_pay = sorted(payload.items())
            sort_pay.sort()
            for k in sort_pay:
                param += '&' + str(k[0]) + '=' + str(k[1])
            param = param.lstrip('&')
        timestamp = str(int(time.time() * 1000))
        full_url = config.fcoin_setting['base_url'] + api_url

        if method == 'GET':
            if param:
                full_url = full_url + '?' +param
            sig_str = method + full_url + timestamp
        elif method == 'POST':
            sig_str = method + full_url + timestamp + param
        signature = self.get_signed(bytes(sig_str, 'utf-8'))
        headers = {
            'FC-ACCESS-KEY': self.key,
            'FC-ACCESS-SIGNATURE': signature,
            'FC-ACCESS-TIMESTAMP': timestamp
        }
        r = {}
        hp = httpcom()
        if method == 'GET':
            r = hp.http_get(full_url, '', headers)
        elif method == 'POST':
            r = hp.http_post(full_url, payload, headers,'json')
        if r and r['status'] == 0:
            return True, r
        else:
            return False, {'error': 'http_pos\'s response.status_code !=200 or exception error', 'data': r}


    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, float):
            raise ValueError('price must be a float!')
        if value < 0 or value > 1000.00:
            raise ValueError('price must between 0~1000.00')
        self._price = value

    # TODO 待实现
    def place(self, **args):
        """
        下单
        """
        self._price = args['price']
        self._amount = args['amount']
        for item in STANDARD_SYMBOL_LIST[:7]:
            self._syms.append( Symbol.convert_to_platform_symbol(Platform.PLATFORM_FCOIN,item))
        status, data = self.buy(config.fcoin_setting['ft']['name'], self._price, self._amount)
        if status ==  True or status == 'success':
            self.time_order = time.time()
            self._log.info('挂买单成功[%s:%s]' % (self._amount, self._price))
            return data
        else:
            error = data['error']
            rdata = data['data']
            sdata = rdata  # json.loads(rdata)
            if isinstance(sdata, dict):
                self._log.info('挂买失败 Errors=%s Status=%s Msg=%s ' % (error, sdata['status'], sdata['msg']))
            else:
                self._log.info('挂买失败 Errors=%s Msg=%s ' % (error, sdata))


    # TODO 待实现
    def cancel(self, order_id, **args):
        """
        撤单
        """
        return self.signed_request('POST', 'orders/{order_id}/submit-cancel'.format(order_id=order_id), **args)


    # TODO 待实现
    def get_order(self, order_id, **args):
        """
        查询订单信息
        """
        return self.signed_request('GET', 'orders/{order_id}'.format(order_id=order_id), **args)


    # TODO 待实现
    def get_orders(self, symbol, states, limit=20, **args):
        """
        查询所有订单信息
        :param symbol:
        :param states: submitted/partial_filled/partial_canceled/canceled/pending_cancel/filled
        :return:
        """
        success, data = self.signed_request('GET', 'orders',symbol=symbol, states=states, limit=limit, **args)
        if success:
    #        print('succeed to list all orders 状态:{0} {1}数据:{2}'.format(states,'\n',data))
            return data['data']
        else:
            print(data)
            return None


    # TODO 待实现
    def get_match_results(self, **args):
        """
        查询订单的成交明细
        """
        return self.signed_request('GET', 'orders/{order_id}/match-results'.format(order_id=self.order_id), **args)

    def _init_log(self):
        self._log = logging.getLogger(__name__)
        self._log.setLevel(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')

        '''
        保存文档
        '''
        handler = logging.FileHandler('fcoin.log')
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self._log.addHandler(handler)

        '''
        控制台显示
        '''
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        self._log.addHandler(console)

    @property
    def gbalance(self):
        """
        获取余额
        :return:
        """
        self._balance = defaultdict(lambda: None)
        success, data = self.get_balance()
        # print(data)
        if success:
            for item in data['data']:
                ava = float(item['available'])
                fro = float(item['frozen'])
                bal = float(item['balance'])
                self._balance[item['currency']] = Balance(ava, fro, bal)
        return self._balance

    def get_account_info(self):
        """
         计算出账户内的余额 再调用写入mysql数据库的方法
        :return:
        """
        coin_traded = {}
        for obj in self.gbalance.items():
            sname = obj[0].upper()
            if sname in SYMBOL:
                coin_traded[sname] = obj[1].available
                print('name=%s availabe=%s frozen=%s balance=%s' % (
                    obj[0], obj[1].available, obj[1].frozen, obj[1].balance))
        return coin_traded


class Balance(object):
    def __init__(self, available=0.0, frozen=0.0, balance=0.0):
        """
        :param available: avaiable
        :type available: float
        :param frozen: frozen
        :type frozen: float
        :param balance: balance
        :type balance: float
        :return:
        """
        self._available = available
        self._frozen = frozen
        self._balance = balance

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        self._available = value

    @property
    def frozen(self):
        return self._frozen

    @frozen.setter
    def frozen(self, value):
        self._frozen = value

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value


if __name__ == '__main__':
    fh = FcoinTransactionHandler()
    # orderdata = fh.place(price=3.000, amount=1) # only for test
    # 获取委托列表中的订单信息
    rdata = fh.get_orders('xrpusdt','submitted')
    if rdata:
        for item in rdata:
            print('{0}{1}'.format('当前委托的订单号：', item['id']))
            cancel = input('打算取消此订单吗 (Y/n)?')
            if cancel.lower() == 'y':
                result = fh.cancel(item['id'])
                print(result)
    # 获取成交历史列表中的已经成交的订单信息
    orders = fh.get_orders('xrpusdt', 'filled')
    for item in orders:
        fh.filled_buy_order_list.append(item)

    # 下单前 查一下余额
    for obj in fh.gbalance.items():
        sname = obj[0].upper()
        if sname in SYMBOL:
            print('name=%s availabe=%s frozen=%s balance=%s' % (obj[0], obj[1].available, obj[1].frozen, obj[1].balance))

    # 下单 按价格分，可能是委托订单
    # print('{0}'.format('打算下订单吗 (Y/n)?'))
    price = 0.0
    buy = input('打算下订单吗 (Y/n)? ')
    if buy.lower() == 'y':
        # print('{0}'.format('请输入挂单价格: '))
        price = float(input('请输入挂单价格: '))
        orderdata = fh.place(price=price, amount=1)
        if orderdata:
            fh.order_list.append(orderdata['data'])
    nlen = len(fh.order_list)
    print('{0}{1}{2}{3}{4}'.format('当前成交的挂买单数量：', nlen, ' ', '挂单价格：', price))
    for i in range(nlen):
        info = fh.get_order(fh.order_list[i])
        print(info)

    # 下单后 获取余额
    for obj in fh.gbalance.items():
        sname = obj[0].upper()
        if sname in SYMBOL:
            print('name=%s availabe=%s frozen=%s balance=%s' % (obj[0], obj[1].available, obj[1].frozen, obj[1].balance))


    # 挂卖单
    success_item_list = []
    amount = 1
    for item in fh.filled_buy_order_list:
        print( 'id={0} symbol={1} amount={2} price={3} fill_fees={4}'.format(item['id'],item['symbol'],item['amount'],item['price'],item['fill_fees']) )
        bsell = input('打算卖掉此订单吗 (Y/n)?')
        if bsell.lower() == 'y':
            price = float(input('请输入卖单价格: '))
            success, data = fh.sell('xrpusdt', price, amount)  # 卖
            if success:
                success_item_list.append(item)
                fh._log.info('挂卖单成功[%s:%s]' % (amount, price))
        else:
            pass




