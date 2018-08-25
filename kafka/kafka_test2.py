#coding: utf8

from python_spiders.kafka import KafkaProducer
import json
import os
import time
import sys
from kafka.errors import KafkaError
import paramiko
from peewee import *
import datetime

pro_db = MySQLDatabase(
    host='xx',
    database='',
    user="",
    passwd="",
    charset='utf8'
)

KAFAKA_HOST = '127.0.0.1'
#'182.92.119.142'
KAFAKA_PORT = 9092
KAFAKA_TOPIC = 'world'



def log(str):
    t = time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime())
    print("[%s]%s" % (t,str))


def Producer(start,end):
    try:
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(KAFAKA_HOST, 22, 'root', 'qmpSjd030116')
        # print('login ok!')
        # cmds =['cd %s'%path,'ls']
        # for cmd in cmds:
        #     stdin, stdout, stderr = ssh.exec_command(cmd)
        #     stdin.write("Y")
        #     out = stdout.readlines()
        #     print(out)
        sql='select words,log_time,nickname from qmp_search_log where log_time>%s and log_time<%s order by log_time desc'
        cur=pro_db.execute_sql(sql,[start,end])
        result=cur.fetchall()
        producer = KafkaProducer(bootstrap_servers='{kafka_host}:{kafka_port}'.format(kafka_host=KAFAKA_HOST,kafka_port=KAFAKA_PORT),
                                 value_serializer=lambda x:json.dumps(x).encode('utf8'))

        # out=os.listdir(path)
        info_dict = {}
        info_list = []

        for x in result:
            f=x[0].encode('utf8')
            s=x[1].encode('utf8')
            n=x[2].encode('utf8')
            info_list.append(f)
            # producer.send(KAFAKA_TOPIC,{'':[f,s,n]})
            # producer.flush()
            # log('send: %s,%s,%s' % (f,s,n))
        info_set = list(set(info_list))
        for x in info_set:
            info_dict[x] = info_list.count(x)

        #按照搜索频次降序展示 reverse=True
        for word,count in sorted(info_dict.items(), key=lambda x:x[1], reverse=False):
            producer.send(KAFAKA_TOPIC, key=word,value=count)
            producer.flush()
            time.sleep(0.1)
            log('send: %s:%s' % (word,count))
        producer.close()

    except KafkaError as e:
        print(e)
if __name__ =='__main__':
    #重复发送
    for i in range(1):
        now=datetime.datetime.now()
        # start='2018-03-12 15:00:00'
        #半小时以内搜索记录minutes=30
        start=(now-datetime.timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
        end=now.strftime('%Y-%m-%d %H:%M:%S')
        Producer(start,end)
        log('结束')