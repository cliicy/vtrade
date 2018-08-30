#  -*- coding:utf-8 -*-
class SignatureUtil:
    """
    签名工具类
    """
    # 公钥字符串
    public_key = None
    # 私钥字符串
    private_key = None
    # 私钥文件
    public_key_file = None
    # 公钥文件
    private_key_file = None
    # 输入字符串
    input_text = None
    # 输出字符串
    output_text = None
    # 验签结果
    verify_result = False
    """
    签名工具类
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
