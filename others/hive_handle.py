#coding:utf8

from peewee import *
import datetime
import pyhs2
import time
import xlwt,xlrd
import happybase

URL_s_db = MySQLDatabase(
    host='47.94.42.90',
    database='shujujiance',
    user="readonly",
    passwd="pqRi2MXjFINsX1UP",
    charset='utf8'
)

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





class Hbase_handle(object):
    # t_name = 'sssss'
    """
    host：主机名
    port：端口
    timeout：超时时间
    autoconnect：连接是否直接打开
    table_prefix：用于构造表名的前缀
    table_prefix_separator：用于table_prefix的分隔符
    compat：兼容模式
    transport：运输模式
    protocol：协议
    """
    def __init__(self):
        self.conn = happybase.Connection(host="###", port=9090)

    def create_t(self,table_name):
        families = {
            "order": dict(),
            "info": dict()
        }
        self.conn.create_table(table_name, families)
        print('create ok!')

    def update_data(self,data,table_name,date):

        if table_name not in self.conn.tables():
            self.create_t(table_name)
        t = self.conn.table(table_name)
        raw_data = {
            'order:info': '%s' % str(data)
        }
        t.put(row=date, data=raw_data)
        print('update hbase data ok!')

    def drop_all_t(self):
        t_list=self.conn.tables()
        for x in t_list:
            #name：表名
            #disable：是否先禁用表
            self.conn.delete_table(x,disable=True)
            print('drop table %s ok!'%x)

    def colse_conn(self):
        self.conn.close()


def main(s_date,e_date):
    # h.exec_query('select count(*) from mf_count_ip')

    query_dict = {
        ##搜索热度
        'S':
            'select words,count(*) as num from search_magic_history where create_time>="%s 00:00:00" and create_time<="%s 23:59:59"  GROUP BY words order by num desc',
        ##人物
        'P':
            "select keywords,count(*) as num from mf_count_ip where visit_time >='%s 00:00:00' and visit_time<='%s 23:59:59' and domain IN ('ios1.api.qimingpian.com','vip.api.qimingpian.com','pro.api.qimingpian.com','wx.api.qimingpian.com','az.qpi.qimingpian.com') AND ( keywords <> '' AND keywords <> '0|' AND keywords not like '%%|'  ) AND method = 'person'  GROUP BY keywords order by num desc",
        ##项目
        'I':
            "select keywords,count(*) as num from mf_count_ip where visit_time >='%s 00:00:00' and visit_time<='%s 23:59:59' and method IN ('c1','c3') AND keywords <> '' AND keywords not like '%%|' AND domain IN ('vip.api.qimingpian.com','ios1.api.qimingpian.com','pro.api.qimingpian.com','wx.api.qimingpian.com','az.api.qimingpian.com') GROUP BY keywords order by num desc",
        ##机构
        'O':
            "select keywords,count(*) as num from mf_count_ip where visit_time >='%s 00:00:00' and visit_time<='%s 23:59:59' and method = 'jigou3info' AND ( keywords <> '汉富资本' AND keywords <> '百场汇' AND keywords <> ''  ) AND domain IN ('vip.api.qimingpian.com','ios1.api.qimingpian.com','pro.api.qimingpian.com','wx.api.qimingpian.com','az.api.qimingpian.com') GROUP BY keywords order by num desc",
        # 非公司产品库
        'C':
            'select keywords,count(*) as num from mf_count_ip_hz left outer join mf_product_company on mf_count_ip_hz.keywords=mf_product_company.company where mf_product_company.company is null and method = "wdproduct" and visit_time >="%s 00:00:00" and visit_time<="%s 23:59:59" GROUP BY keywords order by num desc',

    }
    # now_day = datetime.date.today()
    for s_type in ['I','S','P','O']:

        time.sleep(0.3)

        print(query_dict.get(s_type) %(s_date,e_date))
        try:
            h = Hive_handle()
        except:
            time.sleep(2)
            h = Hive_handle()
        raw_data = h.exec_query(query_dict.get(s_type) % (s_date,e_date))
        h.colse_conn()
        if raw_data:
            dd = []
            for x in raw_data:
                ss = {}
                if len(x[0]) < 3 and s_type == 'C':
                    continue
                ss[x[0].decode('utf8')] = x[1]
                dd.append(ss)

            if s_type == 'I':
                base_name = 'search_item_t'
            elif s_type == 'O':
                base_name = 'search_org_t'
            elif s_type == 'P':
                base_name = 'search_person_t'
            elif s_type == 'S':
                base_name = 'search_history_t'
            else:
                base_name = 'search_company_t'

            date=''.join(s_date.split('-')) if s_date==e_date else base_name + ''.join(s_date.split('-'))+'_'+''.join(e_date.split('-'))
            print(date)
            try:
                hbase = Hbase_handle()
            except:
                print(20*'-'+'ERROR!')
                time.sleep(2)
                hbase = Hbase_handle()
            hbase.update_data(dd, base_name,date)
            hbase.colse_conn()
        else:
            print('data null!!!')

if __name__ == '__main__':
    path = '/Users/qmp/Desktop/hbase_data/'
    now_day = datetime.date.today()-datetime.timedelta(1)
    # e_date='2018-07-12'
    e_date=str(now_day)
    for i in range(3, 0, -1):   #跨度5天统计/3day
        s_date = str(now_day - datetime.timedelta(i))
        print(s_date,e_date)
        main(s_date,e_date)


