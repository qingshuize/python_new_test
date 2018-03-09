#coding:utf8
import os
import sys
import commands
import time


def Easy_test(msg):
    show_cmd = './bin/kafka-topics.sh --list --zookeeper localhost:2181'
    topic_list=commands.getoutput(show_cmd)
    topic_list=topic_list.split('\n')
    topic=topic_list[1]
    print(topic)
    producer_cmd='./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic %s'%topic
    customer_cmd='./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic %s --from-beginning'%topic
    cmd_list='./bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic %s'%topic
    commands.getstatusoutput(producer_cmd)
    # x=input(msg)
    # print(x)
    # s1=commands.getoutput(customer_cmd)
    # info = commands.getoutput(cmd_list)
    # print('info:'+info)




if __name__ =='__main__':
    flag=True
    while flag:
        # msg=input()
        msg='hello!!!'
        print('input messge:'+str(msg))
        os.chdir('/Users/qmp/Desktop/kafka_2.11-1.0.0')
        Easy_test(msg)
        time.sleep(50)
        flag=False
    # os.chdir('/Users/qmp/Desktop/kafka_2.11-1.0.0')
    # show_cmd='./bin/kafka-topics.sh --list --zookeeper localhost:2181'
    # s=commands.getoutput(show_cmd)
    # for i in s.split('\n'):
    #     if not i.startswith('_'):
    #         print('topic:'+i)
    #         if i=='all':
    #             Easy_test(i,msg)