#coding:utf8
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from hbase import Hbase
from hbase.ttypes import *
import datetime,time
import commands
import re,json

from flask import Flask,jsonify,request
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return 'Hi,... ...!'


#http://127.0.0.1:5801/search?stime=0200&etime=1000
#http://127.0.0.1:5801/search?date=20180423

@app.route('/search/<date>',methods=['GET'])
def main(date):
    date_time=datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
    now_date=date_time.split(' ')[0]
    now_time=date_time.split(' ')[-1]
    try:
        date = date if date else now_date
        hbase=Hbase_handle('search_history_order_%s'%date, '39.107.205.65', '9090')
        # hbase = Hbase_handle('add_table', 'localhost', '9090')
        # t_colum=hbase.getColumnDescriptors()
        # print(t_colum)
        # scan=hbase.scanner('order_value:')
        info=hbase.get_late_Row('order_value:')
        # print(info)
        # return Response(data, mimetype='application/json')
        message = 'success'
        status = 0
        data = {
            'data': info,
            'message': message,
            'status': status,
        }
    except:
        data=None

    return jsonify(data)




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

if __name__ == '__main__':
    try:
        # main()

        app.run(debug=True,
                    host='127.0.0.1',
                    port=5801,
                    threaded=True,
                    processes=0,
                    use_debugger=True,
                    use_reloader=False)
    except Exception as e:
        print(type(e))
        if e.args[0]==48:
            print('hahah')
            cmd_pid=commands.getoutput('lsof -i:5800|grep python')
            print(cmd_pid)
            pid=re.findall(r'\d+',cmd_pid)[0]
            print(pid)
            try:
                kill_cmd='kill -9 %s'
                commands.getoutput(kill_cmd%pid)
            except Exception as e:
                print('kill port ok!')


