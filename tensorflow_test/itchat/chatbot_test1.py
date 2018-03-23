#coding:utf8
from wxpy import *
import requests
apikey='43ab5050261d41009a2f51639a168aa2'
api_url='http://www.tuling123.com/openapi/api'

#cache_path 启用缓存
#console_qr 终端内显示二维码
bot = Bot(cache_path=True)
bot.self.send('hi!hahaha!')

# embed()

