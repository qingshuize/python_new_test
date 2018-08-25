#coding:utf8

from peewee import *
import datetime
import pyhs2


class Hive_handle(object):

    def __init__(self):
        # transport = TSocket.TSocket('##', 10000)
        # transport = TTransport.TBufferedTransport(transport)
        # protocol = TBinaryProtocol.TBinaryProtocol(transport)
        # client = ThriftHive.Client(protocol)
        # transport.open()

        self.conn = pyhs2.connect(host='###',
                             port=10000,
                             authMechanism='PLAIN',#NOSASL
                             user='root',
                             password='',
                             database='shujujiance',
                             )

    def exec_query(self,query):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                result=cursor.fetch()
                print(len(result))
                # print(result)
            return result if result else None
                # for s in result:
                #     yield s
        except Exception as e:
            print(e)

    def colse_conn(self):
        self.conn.close()










