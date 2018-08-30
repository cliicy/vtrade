#  -*- coding:utf-8 -*-
from investment.api.utils.signature_util import SignatureUtil
from investment.api.setting import huobi_setting
from investment.api.communicators import HttpCommunicator
import base64
import datetime
import hashlib
import hmac
import urllib
import urllib.parse
import urllib.request
import json
class HuobiUtil(SignatureUtil):
    """
    火币工具类
    """

    def sign(self, *args):
        """
        签名
        :return:
        """
        pass

    def verify(self, *args):
        """
        验证签名
        :return:
        """
        pass

    def api_key_get_params_prepare(self,params, request_path):

        """
            必须需要签名认证的get请求参数整理

        :param params: 请求参数  字典类型
        :param request_path: get请求接口路径 字符串类型
        :return:
            url：实际get请求地址 字符串类型
            params：整理之后的get请求参数 字典类型
            headers_get : get请求headers信息 字典类型
        """
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': huobi_setting['ACCESS_KEY'],
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})
        host_url = huobi_setting['TRADE_URL']
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params['Signature'] = HuobiUtil.createSign(self,params, method, host_name, request_path, huobi_setting['SECRET_KEY'])

        url = host_url + request_path
        headers_get = huobi_setting['GET_HEADERS']

        return url,params,headers_get
        #return http_get_request(url, params)


    def api_key_post_params_prepare(self,params, request_path):

        """
        必须需要签名认证的post请求参数整理

        :param params: 请求参数  字典类型
        :param request_path: post请求接口路径 字符串类型
        :return:
            url：实际post请求地址 字符串类型
            params：整理之后的post请求参数 字典类型
            headers_post : post请求headers信息 字典类型
        """
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': huobi_setting['ACCESS_KEY'],
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}
        host_url = huobi_setting['TRADE_URL']
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = HuobiUtil.createSign(self,params_to_sign, method, host_name, request_path, huobi_setting['SECRET_KEY'])

        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        headers_post = huobi_setting['POST_HEADERS']

        return url, json.dumps(params),headers_post
        #return http_post_request(url, params)


    def createSign(self,pParams, method, host_url, request_path, secret_key):

        """
        签名生成方法
        """
        sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = secret_key.encode(encoding='UTF8')

        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature

    def get_accounts(self):
        """
        :return:
        """
        path = "/v1/account/accounts"
        params = {}
        url, params, headers_post = HuobiUtil.api_key_get_params_prepare(self,params, path)
        return HttpCommunicator.http_get(self,url=url,params=params,headers=headers_post)
if __name__ == '__main__':
    huobi = HuobiUtil()
    print(huobi.get_accounts())