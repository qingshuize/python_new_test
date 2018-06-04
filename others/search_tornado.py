#coding:utf8
import tornado
from tornado.web import RequestHandler,url
from tornado.httpserver import HTTPServer
from tornado.options import options,define
from tornado.ioloop import IOLoop
from peewee import *
import time
import re
import commands
from playhouse.shortcuts import RetryOperationalError


class RetryMySQLDatabase(RetryOperationalError, MySQLDatabase):
    pass

db = RetryMySQLDatabase(
    host='47.94.38.128',
    database='shujujiance',
    user="shujujiance_pyt",
    passwd="f5W1vg##e1cf",
    charset='utf8'
)

define('port',type=int,default=9900,help='port test')

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            url(r'/',Indexhandle,name='index_url'),
            url(r'/info',Infohandle,name='info_url'),
        ]
        settings = {'debug': True}
        tornado.web.Application.__init__(self, handlers, **settings)
class Indexhandle(RequestHandler):
    def set_default_headers(self):
        self.set_header('Contnet-Type','json/html')
    def get(self):
        self.flush()
        self.render('tornado_html/search_ui.html')


class Infohandle(RequestHandler):
    def set_default_headers(self):
        self.set_header('Contnet-Type','json/html')
    def post(self):
        self.flush()
        start = self.get_argument('start_time').replace('T',' ')
        print(start)
        end = self.get_argument('end_time').replace('T',' ')
        print(end)
        num=str(self.get_argument('num'))
        if start and end:
            if start>end:
                self.write('error input!')
            else:
                before_0=time.time()
                words=get_data(start,end,num)
                after_0=time.time()
                time.sleep(0.1)
                # return json.dumps()
                self.render('tornado_html/info.html', words=words, start_time=start,end_time=end,use_time='%.2f s'%(after_0-before_0))

def get_data(start,end,num):
    sql = 'select words,create_time,nickname from search_magic_history where create_time>="%s" and create_time<="%s" order by create_time desc limit %s'%(start, end, num)
    cur = db.execute_sql(sql)
    result = cur.fetchall()
    words=[]
    words_dict={}
    for x in result:
        word=x[0]
        log_time=x[1]
        print(word,log_time)
        words.append(word)
    words_set = list(set(words))
    for x in words_set:
        words_dict[x]=words.count(x)
    #按键值降序排列
    return sorted(words_dict.items(), key=lambda x:x[1],reverse=True)


if __name__=='__main__':
    try:
        options.parse_command_line()
        server = HTTPServer(Application())
        server.listen(options.port)
        IOLoop.current().instance().start()
    except Exception as e:
        print(type(e))
        if e.args[0]==48:
            print('hahah')
            cmd_pid=commands.getoutput('lsof -i:9900|grep python')
            print(cmd_pid)
            pid=re.findall(r'\d+',cmd_pid)[0]
            print(pid)
            try:
                kill_cmd='kill -9 %s'
                commands.getoutput(kill_cmd%pid)
            except Exception as e:
                print('kill port ok!')