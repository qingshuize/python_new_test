# -*-coding:utf-8 -*-
from scrapy.spiders import Spider
from scrapy.http import FormRequest,Request
import re,json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class select_unique(Spider):
    name='unique_spider'
    allowed_domain=['weibo.com']
    headers={
        'Host':'login.sina.com.cn',
        'Origin':'https://weibo.com',
        'Referer':'https://weibo.com/',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded'
    }
    cookies={}
    raw_cookies='SINAGLOBAL=219.142.157.110_1499756849.361004; U_TRS1=00000059.15d861b9.5965f3a5.08cd70ca; UOR=www.baidu.com,blog.sina.com.cn,; SCF=AmTvcM_n8ulzpgm8LtJLEo7WlSEAo6oyLK8Az6WlLbTUY5KE3p5jQs4v5t6Fh-i_9u0DXnOaRFNUsf4V_nNODYE.; vjuids=1f1df62.15d82e3b44a.0.34e9d1d7d5137; SGUID=1501139563872_71163115; lxlrtst=1501462726_o; vjlast=1501670201; lxlrttp=1502410412; ULV=1506757214768:22:2:1::1506077162269; Apache=103.88.46.119_1506757231.7886; SUB=_2AkMuk91-dcNxrAVSn_sdz2vjaYxH-jydRrSIAn7tJhMyAhh87gwvqSV0U8NRR5vWXt8i_yWrNwisRksbWg..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WhBPJnB7U7MAToLxVoPaqOJ5JpV2K27S0q4SK241hx5MP2Vqcv_'
    for cookie in raw_cookies.split(';'):
        cookies[cookie.split('=')[0]]=cookie.split('=')[1]

    raw_formdata='entry=weibo&gateway=1&from=&savestate=7&qrcode_flag=false&useticket=1&pagerefer=https%3A%2F%2Flogin.sina.com.cn%2Fcrossdomain2.php%3Faction%3Dlogout%26r%3Dhttps%253A%252F%252Fweibo.com%252Flogout.php%253Fbackurl%253D%25252F&vsnf=1&su=MTI%3D&service=miniblog&servertime=1506759292&nonce=Y82H7A&pwencode=rsa2&rsakv=1330428213&sp=e670943c476f53aab744492045ffa999e90775e4978ad58608cafc10d6d5516902de627a1f6774787c476b185eb8e39ed51c7f0222173318f4db81ef41da9709b04e1d44fddfa33e278f28b5800d88e9ed07d1dd9970574776ef889c3dd290a2059418e2c89ba258ad3bbb302e7e610b32f96f20e0ee5ac4d953fd93ef4d22aa&sr=1280*800&encoding=UTF-8&cdult=2&domain=weibo.com&prelt=20&returntype=TEXT'
    formdata={}
    for f_data in raw_formdata.split('&'):
        formdata[f_data.split('=')[0]]=f_data.split('=')[1]

    def get_cookies(self):
        login_url=''


    def start_requests(self):
        url='https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&_=1506759290132'
        yield FormRequest(url=url,headers=self.headers,cookies=self.cookies,formdata=self.formdata
                          )

    def parse(self, response):
        res=response.body_as_unicode()
        data=json.loads(res)
        print('raw_reason:'+data['reason'])