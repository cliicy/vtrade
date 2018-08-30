#  -*- coding:utf-8 -*-
import urllib
import urllib.parse
import urllib.request
import requests
import json

class HttpCommunicator:
    """
    http通信器
    """
    def http_get(self,url,params,headers):

        """
         http通信器get请求方法

        :param url: 请求接口地址 字符串类型 例如：'https://api.huobi.pro/market/history/kline'
        :param params: 请求参数  字典类型  例如：{'symbol': 'btcusdt', 'period': '1min', 'size': 150}
        :param headers: 请求头信息  字典类型 例如：{'Content-type': 'application/x-www-form-urlencoded',
                                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
        :return: 返回json格式数据
        """
        # headers = headers
        # postdata = urllib.parse.urlencode(params)

        headers = headers
        postdata = params
        response = requests.get(url, postdata, headers=headers, timeout=5)
        try:

            if response.status_code == 200:
                return response.json()
            else:
                print(response.status_code)
                return
        except BaseException as e:
            print("httpGet failed, detail is:%s,%s" % (response.text, e))
            return


    def http_post(self, url, params, headers, content_type=None, timeout=10):

        """
        http通信器post请求方法

        :param url: 请求接口地址 字符串类型 例如：'https://api.huobi.pro/market/history/kline'
        :param params: 请求参数  字典类型  例如：{'symbol': 'btcusdt', 'period': '1min', 'size': 150}
        :param headers: 请求头信息  字典类型 例如：{'Content-type': 'application/x-www-form-urlencoded',
                                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
        :return: 返回json格式数据
        """

        headers = headers
        postdata = params
        #postdata = json.dumps(params)
        #print('url')
        #print(url)
        if content_type is not None:
            response = requests.post(url, None, postdata, headers=headers, timeout=timeout)
        else:
            response = requests.post(url, postdata, headers=headers, timeout=timeout)
        try:
            print(response.text)
            if response.status_code == 200:
                return response.json()
            else:
                return
        except BaseException as e:
            print("httpPost failed, detail is:%s,%s" % (response.text, e))
            return


class SocketCommunicator:
    """
    socket通信器
    """
    # TODO 待开发