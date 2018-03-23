#coding:utf8
# import multiprocessing
import sys
import time
import json
from tensorflow_test.kafka import *
from kafka.errors import KafkaError

KAFAKA_HOST = '127.0.0.1'
KAFAKA_PORT = 9092
KAFAKA_TOPIC = 'new'

class Kafka_producer():

    def __init__(self, host,port, topic, key):
        self.kafkaHost = host
        self.kafkaPort = port
        self.kafkatopic = topic
        self.key = key
        self.producer = KafkaProducer(bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
                                        kafka_host=self.kafkaHost,
                                        kafka_port=self.kafkaPort)
                        )

    def sendjsondata(self, params={}):
        try:
            parmas_message = json.dumps(params)
            producer = self.producer
            producer.send(self.kafkatopic, key=self.key, value=parmas_message.encode('utf-8'))
            producer.flush()
        except KafkaError as e:
            print(e)



class Kafka_consumer():

    def __init__(self, host, port, topic, groupid):
        self.kafkaHost = host
        self.kafkaPort = port
        self.kafkatopic = topic
        self.groupid = groupid
        self.consumer = KafkaConsumer(self.kafkatopic, group_id=self.groupid,
                                      bootstrap_servers='{kafka_host}:{kafka_port}'.format(
                                          kafka_host=self.kafkaHost,
                                          kafka_port=self.kafkaPort)
                                      )

    def consume_data(self):
        try:
            for message in self.consumer:
                yield message
        except KeyboardInterrupt as e:
            print(e)




def main(xtype,group):
    try:
        if xtype == "P":
            while True:
                key=raw_input('input message:')
                producer = Kafka_producer(KAFAKA_HOST, KAFAKA_PORT, KAFAKA_TOPIC, key)
                print(20 * '*' + 'producer' + 20 * '*')
                for _id in range(3):
                # params = '{"msg" : "%s"}' % str(_id)
                    producer.sendjsondata()
                time.sleep(0.5)
                producer.close()

        if xtype == 'C':
            consumer = Kafka_consumer(KAFAKA_HOST, KAFAKA_PORT, KAFAKA_TOPIC,group)
            print(20*'-'+'consumer'+20*'-')
            print('group:'+group)
            message = consumer.consume_data()
            for msg in message:
                print('msg: '+str(msg))
                print('key: '+str(msg.key))
                timestamp=msg.timestamp
                date_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestamp/1000))
                print('time:'+date_time)
                # print('offset: '+str(msg.offset))
    except Exception as e:
        print(e)


#生产者模式
def worker(ch):
    producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')

    for i in range(1000):
        time.sleep(0.01)
        print 'produce msg', i
        producer.send('publish_msg', ch * 1024)


if __name__ == '__main__':
    xtype = sys.argv[1]
    group = sys.argv[2]
    main(xtype,group)


    # p1 = multiprocessing.Process(target=worker, args=('1',))
    # p2 = multiprocessing.Process(target=worker, args=('2',))
    # p1.start()
    # p2.start()