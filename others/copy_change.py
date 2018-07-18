#coding:utf8
from peewee import *
import commands
import re
import time
import signal
qmpnews_db = MySQLDatabase(
   ##

def copy_url_s():
    path='/alidata1/www/pdf1.qimingpian.com/announcement_real/'
    sql='select url from mf_file_list where is_watermark=1 limit 10'
    update_sql='update mf_file_list set url=replace(url,"announcement","announcement_real") where is_watermark=1'
    cusor=qmpnews_db.execute_sql(sql)
    ress=cusor.fetchall()
    for x in ress:
        r_path=x[0].encode('utf8')
        print(r_path)
    #     file_p=re.findall('announcement/(.*).pdf',r_path)[0]+'.pdf'
    #     print(file_p)
    #     commands.getoutput('mv %s %s'%(r_path.repalce('http://','/alidata1/www/'),path+file_p))
    # qmpnews_db.execute_sql(update_sql)
    # print('update ok!')

def after_timeout(i):  # 超时后的处理函数
    print("timeout!!!.")
    print(i)

#超长时间处理
def timeout_error(interval,callback,i):
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(interval)  # 设置 num 秒的闹钟
                r = func(*args, **kwargs)
                signal.alarm(0)
                return r
            except RuntimeError as e:
                print(e)
                callback(i)

        return to_do

    return wrap

@timeout_error(3,after_timeout,'j')
def test_timeout():
    for i in range(1000):
        time.sleep(2)
        print('i:'+str(i))

if __name__ == '__main__':
    # copy_url_s()
    for _ in range(4):
        print('start!!')
        test_timeout()

