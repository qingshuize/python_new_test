#coding:utf8

import requests
from lxml import etree
import time

def get_spiderkeeper():
    headers={
        'Host':'123.206.29.196',
        'Cookie':'session=eyJwcm9qZWN0X2lkIjoiMSJ9.DdGTvg.4HwfsrVbsqXrxl0O2ncmtuKdexQ',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
        'Accept-Language':'zh-cn',
        'Accept-Encoding':'gzip, deflate',
        'Authorization':'Basic YWRtaW46cnFwNndnYXEjMQ==',
    }
    Authentication={
        'Server':{'Basic Authentication':{'User ID':'admin','Password':'rqp6wgaq#1'}}
    }
    pro_item={'1':'liebao_spider',
              '2':'secondary_market'
    }
    for pro_id,pro in pro_item.items():
        url='http://123.206.29.196/project/%s/job/dashboard'%pro_id
        headers['Referer']='http://123.206.29.196/project/%s/job/dashboard'%pro_id
        res = requests.get(url,headers=headers)
        print(20*"//"+'spider project:'+pro+20*"//")
        if res.status_code==200:
            raw_data=etree.HTML(res.text)
            #等待运行/html/body/div/div[1]/section[2]/div[1]/div[2]/table
            # 正在运行/html/body/div/div[1]/section[2]/div[2]/div[2]/table
            item_types=['pending','running']
            for item_type in item_types[:1]:
                try:
                    print('data type:'+item_type)
                    i='1' if item_type=='pending' else '2'
                    info_data=raw_data.xpath('//body/div/div[1]/section[2]/div[%s]/div[2]/table/tr'%i)
                    for detail in info_data[1:]:
                        running_spiders_list=detail.xpath('td[3]/text()')
                        runtime_list=detail.xpath('td[4]/text()')
                        if running_spiders_list and runtime_list:
                            running_spiders=running_spiders_list[0].replace(' ','')
                            print(running_spiders)
                            runtime=runtime_list[0].replace(' ','')
                            print(runtime)
                except Exception as e:
                    print(e)
    print(30*'-'+'END'+30*'-')
if __name__ == '__main__':
    for _ in range(5):
        get_spiderkeeper()
        time.sleep(3)