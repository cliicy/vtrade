# -*- coding:utf-8 -*-
from cryptography.fernet import Fernet
from config import CryptoConfig
import base64
import hashlib


class CryptoUtil(object):

    @staticmethod
    def encrypt(text):
        # cipher_key = Fernet.generate_key()
        cipher_key = CryptoConfig.account_cipher_key.encode('utf-8')
        cipher = Fernet(cipher_key)
        return str(cipher.encrypt(text.encode(encoding='utf-8')), 'utf-8')

    @staticmethod
    def decrypt(text):
        cipher_key = CryptoConfig.account_cipher_key.encode('utf-8')
        cipher = Fernet(cipher_key)
        return str(cipher.decrypt(text.encode(encoding='utf-8')), 'utf-8')

    @staticmethod
    def md5_encrypt(text):
        m = hashlib.md5()
        bytes = text.encode(encoding='utf-8')
        m.update(bytes)
        return m.hexdigest()

    @staticmethod
    def base64_encrypt(text):
        encrypt_str = base64.b64encode(text.encode('utf-8'))
        return str(encrypt_str, 'utf-8')

    @staticmethod
    def base64_decrypt(text):
        decode_str = base64.b64decode(text.encode('utf-8'))
        return str(decode_str, 'utf-8')


if __name__ == '__main__':
    # a = CryptoUtil().md5_encrypt(base64_encrypt)
    # print(a)
    # str = "aaaa"
    # bytes = str.encode(encoding='utf-8', errors='strict')
    # print(CryptoUtil().md5_encrypt(CryptoUtil().base64_encrypt("dfyg@1234")))
    print(CryptoUtil().base64_encrypt("dfyg@1234"))
    print(CryptoUtil().base64_decrypt("ZGZ5Z0AxMjM0"))
    print(CryptoUtil().encrypt("ZGZ5Z0AxMjM0"))
    print(CryptoUtil().decrypt('gAAAAABbf-Bc5RqxWfYdPmg7IczJsjlXIPoq2k3NAcUPAC5bTqiCN8iaCpuJBnAI3h60e7Y__aGHdUImy83ZmtEU5SmvIe01tQ=='))
