#coding:utf8
import time
import datetime
import happybase
import commands
import re
from flask import Flask,jsonify,request
from pdf_add_watermark import *
import webbrowser
sys.path.append("libs")
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


#hbase获取搜索热度排行
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
            'data': None,
            'update_time': now_time,
            'message': 'input data error!',
            'status': -1,
        }
        return jsonify(data)
    else:
        if date=='today':
            print('date:', date)
            date = date_time

       # uery_str = "SingleColumnValueFilter ('order_value:','',=, 'regexstring:(^%s35)', true, false)"%hour
        if date==date_time:
            select_hour=hour if mintues>=35 else hour-1
            select_hour=str(select_hour)
            select_hour='0'+select_hour if len(select_hour)==1 else select_hour
        else:
            select_hour=23
        print(select_hour)

        try:
            tablename = 'search_history_order_%s' % date
            conn = happybase.Connection('39.107.205.65')
            table = conn.table(tablename)
            colum = 'order_value:'
            filter = "RowFilter(=,'regexstring:^%s')" % select_hour
            ## 列匹配
            # filter = "FuzzyRowFilter(=,'regexstring:^%s')"% select_hour
            query = table.scan(filter=filter)
            result = list(query)
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
            data=item[:n]
            # 关闭连接
            conn.close()
        except:
            data=None

        timestamp=(date[:4]+'-'+date[4:-2]+'-'+date[-2:]+' '+str(select_hour)+':'+'35'+':'+'00')
        status, message = (0, 'success') if data else (-1, 'service failed')    #可能thriftserver关闭导致
        data={
            'data':data,
            'update_time':timestamp,
            'message': status,
            'status': message,
        }
        return jsonify(data)


@app.route('/pdf_download',methods=['GET'])
def ADD_watermark2pdf():
    link=request.values['link']
    pdf_obj = PDF_watermark_handle()
    pdf_obj.create_word_watermark('天空飘来五个字？','test0')
    file_name=pdf_obj.get_url_content(link)
    out_dest=pdf_obj.add_watermark(file_name,'test0.pdf','output/')
    return '''
    <html>
    <head>
    <body>
    <a href="file://%s" download="dowload_pdf"><strong>pdf download</strong></a>
    </body>
    </html>
    '''%(out_dest)




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
        """
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
	"""
