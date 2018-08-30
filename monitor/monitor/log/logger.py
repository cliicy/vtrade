#  -*- coding:utf-8 -*-
import logging
import os.path
import time
from config import LogConfig
import logging.handlers

class Logger(object):
    def __init__(self, logger):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        :param logger:
        """
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建日志名称。
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))
        # os.getcwd()获取当前文件的路径，os.path.dirname()获取指定文件路径的上级路径
        log_path = LogConfig.file_path
        log_name = log_path + rq + '.log'
        # 创建一个handler，用于写入日志文件
        print(log_name)
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # socket
        sh = logging.handlers.SocketHandler('localhost',

                                                       logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        sh.setLevel(logging.INFO)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.addHandler(sh)

    def getlog(self):
        return self.logger
if __name__ == '__main__':
    logger = Logger(__name__).getlog()
    logger.debug("aaa")
    logger.info("bbb")