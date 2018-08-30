#  -*- coding:utf-8 -*-
from investment.api.utils.signature_util import SignatureUtil
import hashlib
from investment.api.setting import okcoin_setting

class OkcoinSignatureUtils(SignatureUtil):
    """
    okcoin签名工具类
    """
    @staticmethod
    def sign(params):
        """
        签名
        """
        sign = ''
        for key in sorted(params.keys()):
            sign += key + '=' + str(params[key]) + '&'
        data = sign + 'secret_key=' + okcoin_setting['secretkey']
        return hashlib.md5(data.encode("utf8")).hexdigest().upper()

    @staticmethod
    def verify(self, *args):
        """
        验证签名
        """
        # TODO 待完成

