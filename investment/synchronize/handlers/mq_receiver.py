#  -*- coding:utf-8 -*-
#  -*- coding:utf-8 -*-
import pika
from config import DBConfig as Config
from investment.enums import Platform, PlatformDataType

class MqReceiver:
    queue_name_prefix = "default"

    def __init__(self, platform, data_type):
        """
        队列消费者初始化
        :param platform: 平台
        :param data_type: 数据类型
        """
        self.queue_name_prefix = '%s_%s' % (platform, data_type)

    def receive(self, syn_method, topic="_m"):
        """
        数据获取
        :return:
        """
        username = Config.RABBITMQ_USERNAME  # 指定远程rabbitmq的用户名密码
        pwd = Config.RABBITMQ_PWD
        user_pwd = pika.PlainCredentials(username, pwd)
        s_conn = pika.BlockingConnection(pika.ConnectionParameters(Config.RABBITMQ_HOST, credentials=user_pwd))  # 创建连接
        chan = s_conn.channel()  # 在连接上创建一个频道
        chan.exchange_declare(
            exchange='db_type',
            exchange_type='topic'
        )
        queue_name = self.queue_name_prefix+topic
        chan.queue_declare(queue=queue_name)  # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
        print(queue_name)
        def callback(ch, method, properties, body):  # 定义一个回调函数，用来接收生产者发送的消息
            syn_method(body)

        binding_key = self.queue_name_prefix
        chan.queue_bind(exchange='db_type',
                           queue=queue_name,
                           routing_key=binding_key)
        chan.basic_consume(callback,  # 调用回调函数，从队列里取消息
                           queue=queue_name,  # 指定取消息的队列名
                           no_ack=True)  # 取完一条消息后，不给生产者发送确认消息，默认是False的，即  默认给rabbitmq发送一个收到消息的确认，一般默认即可
        print('[消费者] waiting for msg .')
        print(binding_key)
        chan.start_consuming()  # 开始循环取消息

    def sync_data(self, data):
        print("[消费者] recv %s" % data)


if __name__ == '__main__':
    mqr = MqReceiver(Platform.PLATFORM_BINANCE.value, PlatformDataType.PLATFORM_DATA_KLINE.value)
    mqr.receive(mqr.sync_data)
