#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from hbase import Hbase
from hbase.ttypes import *
import datetime,time
import re,json
import happybase
import commands
from peewee import *


from flask import Flask,jsonify,request
app=Flask(__name__)

db = MySQLDatabase(
##########
)

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
        hbase=Hbase_handle('search_history_order_%s'%date, '123.206.77.49', '9090')
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


def select_com():
    sql='select company,yewu'

def Hbase_controller(tag,date,num=1,size=20):
    if tag == 's':
        base_t = 'search_history_t'
    elif tag == 'i':
        base_t = 'search_item_t'
    elif tag == 'o':
        base_t = 'search_org_t'
    elif tag == 'p':
        base_t = 'search_person_t'
    else:
        base_t = 'search_company_t'

    try:
        # conn = happybase.Connection(host="###", port=9090, timeout=None, autoconnect=True
        #                             , table_prefix=None, table_prefix_separator=b'_', compat='0.98',
        #                             transport='buffered', protocol='binary')
        pool = happybase.ConnectionPool(size=5,host="###", port=9090)
        with pool.connection() as conn:
            colum = 'order:info'
            table = happybase.Table(base_t, conn)
            content = table.row(date, [colum],include_timestamp=False)
            print(type(content))
            raw_data = eval(content[colum])
            # print(type(raw_data))
            print('total items:' + str(len(raw_data)))
            # 截取前num条数据
            if num == 'all':
                n = None
                size=1
            else:
                n = int(num)
                size=int(size)
            data = raw_data[(n-1):n*size]

            # 关闭连接
            conn.close()
    except Exception as e:
        print(e)
        data = None
    return data

"""
    date:日期，从20170101到20170104，参数形式如（20170101|20170104），一天形如20170401或today（当天）
    page：页码
    size：每页显示数目
    tag：搜索项目（搜索热度（s），用户浏览人物（p），项目（i），机构排行（o），合作调用接口分析无产品公司排名（c））
"""
@app.route('/date/<date>/show/<page>/<size>/tag/<tag>',methods=['GET'])
def Main(date,page,size,tag='s'):

    now_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_time=datetime.date.today().strftime('%Y%m%d')
    date_list=date.split('|')
    flag=0
    if len(date_list)!=1:
        s_date=date_list[0]
        e_date=date_list[1] if date_list[1] else date_time
        flag=1
    else:
        date = date_time if date == 'today' else date
        s_date=e_date= date


    if s_date>date_time or s_date<'20180401':
        data = {
            'data': None,
            'update_time': now_time,
            'message': 'input data error',
            'status': -1,
        }
        return jsonify(data)
    else:

        hms=' 23:55:00'
        hms_n=datetime.datetime.now().strftime(" %H:%M:%S")
        ymr = e_date[:4]+'-'+e_date[4:-2]+'-'+e_date[-2:]
        timestamp=ymr+hms if flag==1 else ymr+hms_n
        input_date=s_date+'_'+e_date if flag==1 else s_date

        data=Hbase_controller(tag,input_date,page,size)
        status,message=(0,'success') if data else (-1,'service failed')     ##可能thriftserver down导致
        data={
            'data':data,
            'update_time':timestamp,
            'message': message,
            'page':page,
            'size':size,
            'status': status,
        }
        return jsonify(data)

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
        print(e)
        if e.args[0]==48:
            print('hahah')
            cmd_pid=commands.getoutput('lsof -i:5801|grep python')
            print(cmd_pid)
            pid=re.findall(r'\d+',cmd_pid)[0]
            print(pid)
            try:
                kill_cmd='kill -9 %s'
                commands.getoutput(kill_cmd%pid)
            except Exception as e:
                print('kill port ok!')


