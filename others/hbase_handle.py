#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from hbase import Hbase
from hbase.ttypes import *
import time
import json





def time2stamp(x,flag):
    #生成时间戳
    #flag=0 日期时间
    #flag=1 日期
    #其他 时间
    print(x)
    format_style="%Y%m%d %H:%M:%S" if flag==0 else "%Y%m%d" if flag==1 else "%H:%M:%S"
    datetimeArray = time.strptime(x, format_style)
    timestamp = int(time.mktime(datetimeArray)/1000)
    print(timestamp)
    return timestamp

def stamp2time(x,flag):
    # 时间戳转换为日期时间
    # flag=0 日期时间
    # flag=1 日期
    # 其他 时间
    format_style = "%Y%m%d %H:%M:%S" if flag == 0 else "%Y%m%d" if flag == 1 else "%H:%M:%S"
    if flag==0:
        time_local = time.localtime(x)
        # 转换成新的时间格式(xxxx-xx-xx xx:xx:xx)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    elif flag==1:
        dt=None
    else:
        m,s=divmod(x,60)
        h,m=divmod(m,60)
        dt="%02d:%02d:%02d" % (h, m, s)
    return dt



class Hbase_handle(object):
    def __init__(self,table,host,port):
        self.table = table.encode('utf-8')
        self.host = host
        self.port = port
        # server端地址和端口,web是HMaster也就是thriftServer主机名,9090是thriftServer默认端口
        self.transport = TSocket.TSocket(host,port)
        self.transport.setTimeout(5000)
        # 设置传输方式（TFramedTransport或TBufferedTransport）
        self.trans = TTransport.TBufferedTransport(self.transport)
        # 设置传输协议
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.trans)
        # 确定客户端
        self.client = Hbase.Client(self.protocol)
        # 打开连接
        self.transport.open()

    def __del__(self):
        self.transport.close()

    def getColumnDescriptors(self):
        return self.client.getColumnDescriptors(self.table)


    # 获取最新一条记录
    def get_late_Row(self, column):
        dic = {}
        try:
            id = self.client.scannerOpen(self.table, "", [column, ])
            r = self.client.scannerGetList(id, 50)
            # print(len(r))
            info = r[len(r) - 1]
            row_key = info.row
            print(row_key)
            value = json.loads(info.columns[column].value)
            dic['item'] = value
            timestamp = info.columns[column].timestamp
            date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1000))
            dic['timestamp'] = date_time.decode('utf-8')
            print("get row finished")
        except Exception as e:
            print(e)
        return dic

    # 获取所有记录
    def scanner(self, column):
        result = []
        try:
            id = self.client.scannerOpen(self.table, "", [column, ])
            r = self.client.scannerGetList(id, 30)
            print(len(r))
            info = r[len(r) - 1]
            print(info)
            while info:
                dic = {}
                try:
                    info = info[0]
                    row_key = info.row
                    s = info.columns[column]
                    timestamp = s.timestamp
                    date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1000))
                    dic['timestamp'] = date_time.decode('utf-8')
                    value = json.loads(s.value)
                    dic['data'] = value
                    result.append(dic)
                    info = self.client.scannerGet(id)
                except Exception as e:
                    print(e)
            print("scanner finished")
        except Exception as e:
            print(e)

        return result



