#coding:utf8

from tensorflow_test.kafka import KafkaConsumer
from kafka.errors import KafkaError
import time
import paramiko
import re,json

KAFAKA_HOST = '127.0.0.1'
#'182.92.119.142'
KAFAKA_PORT = 9092
KAFAKA_TOPIC = 'world'

def log(str):
    t = time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime())
    print("[%s]%s" % (t, str))

def Consumer():
    try:
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(KAFAKA_HOST, 22, 'root', 'qmpSjd030116')
        # print('login ok!')
        # cmd='ls'
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # stdin.write("Y")
        # out = stdout.readlines()
        log('start consumer')
        consumer = KafkaConsumer(KAFAKA_TOPIC,bootstrap_servers=['{kafka_host}:{kafka_port}'.format(kafka_host=KAFAKA_HOST,kafka_port=KAFAKA_PORT)])
        for x in consumer.topics():
            print('topic:'+x)
        for msg in consumer:
            # try:
            #     info=json.loads(msg.value)
            #     # if info.values()[0][-1]==u'Doris':
            #     word=info.values()[0][0]
            #     print('word: %s'%word)
            # except Exception as e:
            #     print(e)
            # info=json.loads(msg.value)
            # word=info.keys()[0]
            # numbers=info.values()[0]
            recv = u"topic:%s partition:%d offset:%d: 搜索词:%s 搜索频次:%s" % (msg.topic, msg.partition, msg.offset,(msg.key).decode('utf8'),msg.value)
            log(recv)

    except Exception as e:
        print(e)

if __name__ == '__main__':
    Consumer()