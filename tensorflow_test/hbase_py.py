#coding:utf8
import time
import datetime
import happybase
import commands
import re
from flask import Flask,jsonify
app=Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return 'Hi!'

def stamp2time(x,flag):
    # 时间戳转换为日期时间
    # flag=0 日期时间
    # flag=1 日期
    # 其他 时间
    format_style = "%Y-%m-%d %H:%M:%S" if flag == 0 else "%Y-%m-%d" if flag == 1 else "%H:%M:%S"
    if flag==0:
        time_local = time.localtime(x)
        # 转换成新的时间格式(xxxx-xx-xx xx:xx:xx)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    elif flag==1:
        pass
        dt=None
    else:
        m,s=divmod(x,60)
        h,m=divmod(m,60)
        dt="%02d:%02d:%02d" % (h, m, s)
    return dt

def time2stamp(x,flag):
    #生成时间戳
    #flag=0 日期时间
    #flag=1 日期
    #其他 时间
    print(x)
    format_style="%Y-%m-%d %H:%M:%S" if flag==0 else "%Y%m%d" if flag==1 else "%H:%M:%S"
    datetimeArray = time.strptime(x, format_style)
    timestamp = int(time.mktime(datetimeArray))
    return timestamp


@app.route('/time/<date>/show/<num>',methods=['GET'])
def Hbase_get(date,num):
    now_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_time=datetime.date.today().strftime('%Y%m%d')
    print(date_time)
    hour=time.localtime().tm_hour
    print('hour:',hour)
    mintues=time.localtime().tm_min
    print('mintues:',mintues)
    if (date>date_time or date<'20180416') and date!='today':
        data = {
            'data': 'input data error!',
            'update_time': now_time,
            'message': 'failed',
            'status': -1,
        }
        return jsonify(data)
    else:
        if date=='today':
            print('date:', date)
            date = date_time
        tablename='search_history_order_%s'%date
        conn = happybase.Connection('39.107.205.65')
        table = conn.table(tablename)
        colum='order_value:'
        ## 列匹配
        # query_str = "SingleColumnValueFilter ('order_value:','',=, 'regexstring:(^%s35)', true, false)"%hour
        if date==date_time:
            select_hour=hour if mintues>=35 else hour-1
        else:
            select_hour=23
        filter = "RowFilter(=,'regexstring:^%s')" % select_hour
        # filter = "FuzzyRowFilter(=,'regexstring:^%s')"% select_hour
        query = table.scan(filter=filter)
        result = list(query)

        #关闭连接
        # conn.close()

        # # print(result)
        row_key=result[0][0]
        print(row_key)
        # timestamp=result
        # print(timestamp)
        value_data=result[0][1].get(colum)
        item=eval(value_data)
        # print(type(item))
        print('total items:'+str(len(item)))
        #截取前num条数据
        if num=='all':
            n=None
        else:
            n=int(num)
        timestamp=(date[:4]+'-'+date[4:-2]+'-'+date[-2:]+' '+str(select_hour)+':'+'35'+':'+'00')
        data={
            'data':item[:n],
            'update_time':timestamp,
            'message': 'success',
            'status': 0,
        }
        return jsonify(data)
if __name__ == '__main__':
    try:
        # Hbase_get()
        app.run(debug=True,
                host='127.0.0.1',
                port=5800,
                threaded=True,
                processes=0,
                use_debugger=True,
                use_reloader=True)
    except Exception as e:
        print(e)
        try:
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
        except:
            pass