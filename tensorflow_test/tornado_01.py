#coding:utf8
from tornado.web import RequestHandler,url,UIModule
from tornado.httpserver import HTTPServer
from tornado.httpclient import HTTPClient
from tornado.ioloop import IOLoop
from tornado.options import options,define
import os,hashlib
import tornado.web
import time
import pymongo,json,datetime
import urllib

define('port',type=int,default=7800,help='port test')
#tornado.options.options.define('type',type=str,default=[],multiple=True,help='type test')

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            url(r'/',Indexhandle,name='index_url'),
            url(r'/index1', Index1handle, name='index1_url'),
            url(r'/index2',Index2handle,name='index2_url'),
            url(r'/mongo/(\w+)',Wordhandle,name='mongourl'),
            url(r'/info',Infohandle,name='info_url'),
            url(r'/async',AsyncHandler,name='asyn')
        ]
        settings=dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={'index2':Indexmodule,'test':Testmodule,'info':Infomodule},
            debug=True,
        )
        conn = pymongo.MongoClient("localhost", 27017)
        #self.db = conn["example"]
        self.db=conn['info']
        tornado.web.Application.__init__(self,handlers,**settings)


class Indexhandle(RequestHandler):
    def set_default_headers(self):
        self.set_header('Contnet-Type','json/html')
    def get(self):
        self.render('index.html')
        # arg=self.get_argument('a','welcome',strip=False)
        # #args=self.get_arguments('q',strip=False)
        # #arg=self.get_body_argument('q')
        # #self.write(str(args)+'\n')
        # self.write(arg+'<br>')
        # self.write('Hello!')
        # self.set_header('haa','lalal')

class Index1handle(RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.write('<strong>Error!</strong><br>')
        self.write('错误码:%s<br>'%kwargs.get('error_name',''))
        self.write('错误信息:%s<br>'%kwargs.get('error_content',''))

    def get(self):
        error_info={
            'error_name':'错误信息 not found',
            'error_content':'错误内容未知！！！'
        }
        self.send_error(305,**error_info)
    def post(self):
        p1=self.get_argument('input1')
        p2 = self.get_argument('input2')
        passwd=hashlib.sha1(p2).hexdigest() if p2 else p2
        p3=self.get_argument('text_data')
        p4=self.get_argument('link')
        self.render('index1.html',input1=p1,input2=passwd,input3=p3,input4=p4)
        #self.write('<form method="post" action="/"><input type="submit" value="login"></form>')
        #self.redirect(self.reverse_url('index_url'))

class Indexmodule(UIModule):
    def render(self):
        return '<p><a href="#">This uimodule</a></p>'

class Testmodule(UIModule):
    def render(self,test):
        return self.render_string('../modules/test.html',test=test)

    def html_body(self):
        return "<div class='addition'><p>html_body()</p></div>"

    def embedded_javascript(self):
        return "document.write(\"hi!\")"

    def embedded_css(self):
        return ".addition {background-color:#F5F5FF}"

    def css_files(self):
        return "/static/css/text.css"

    # def javascript_files(self):
    #     return "/static/js/sample.js"


class Index2handle(RequestHandler):
    def get(self):
        self.render('index2.html',test={
            'name': 'john',
            'link': 'https://www.csdn.net/',
            "time":time.time(),
        })

class Wordhandle(RequestHandler):
    def get(self,word):
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            del word_doc['_id']
            self.write(word_doc)
        else:
            self.set_status(400)
            self.write({'info':'error!'})


class Infohandle(RequestHandler):
    def get(self):
        self.render(
            'recommend_post.html',
            title='one',
            source='receive data')

    def post(self):
        name=self.get_argument('name','')
        page=self.get_argument('page','')
        price=self.get_argument('price','')
        add_data={
            'name':name,
            'page':page,
            'price':price
        }
        if '' not in add_data.itervalues():
            coll = self.application.db.info
            if not coll.find_one({'name':name}):
                coll.insert(add_data)
                data = coll.find()
                self.render(
                    'recommend.html',
                    info=data,
                    title='one',
                    source='receive data')

            if coll.find_one(add_data):
                self.write('<script>alert("error! is exist!")</script>')

        else:
            self.write('<script>alert("null! input again!")</script>')


class Infomodule(UIModule):
    def render(self,info):

        return self.render_string(
            '../modules/info.html',
            info=info,
        )
class AsyncHandler(RequestHandler):
    def get(self):
        query = self.get_argument('q')
        client = HTTPClient()
        response = client.fetch("http://search.twitter.com/search.json?" + urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100}))
        body = json.loads(response.body)
        result_count = len(body['results'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['results'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                "%a, %d %b %Y %H:%M:%S +0000")
        seconds_diff = time.mktime(now.timetuple()) - time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count) / seconds_diff
        self.write("""
        <div style="text-align: center">
            <div style="font-size: 72px">%s</div>
            <div style="font-size: 144px">%.02f</div>
            <div style="font-size: 24px">tweets per second</div>
        </div>""" % (query, tweets_per_second))

if __name__=='__main__':
    options.parse_command_line()
    #tornado.options.options.parse_config_file('./config')
    #print(tornado.options.options.type)
    # app=Application(
    # handlers=[
    #     url(r'/',Indexhandle,name='index_url'),
    #     url(r'/index',Index1handle,name='inedx1_url')
    # ],
    # template_path=os.path.join(os.path.dirname(__file__), "templates"),
    # static_path=os.path.join(os.path.dirname(__file__), "static"),
    # debug=True)
    server=HTTPServer(Application())
    #app.listen(8001)
    #server.bind(tornado.options.options.port)
    #server.start(0)
    server.listen(options.port)
    IOLoop.current().start()