#coding:utf8
from scrapyd_api import ScrapydAPI
import requests
from lxml import etree
import time

def get_scrapyd_list(addr_data):
    addr='http://%s:6800' % addr_data[0]
    name=addr_data[1]
    s=ScrapydAPI(addr)
    print(20*"-"+name+' addr:%s'%addr+20*'-')
    list_pro=s.list_projects()
    for pro in list_pro:
        try:
            list_job=s.list_jobs(pro)
            # running_job=list_job.get('running')
            pending_jobs=list_job.get('pending')
            # finished_job = list_job.get('finished')
            if pending_jobs:
                for pending_job in pending_jobs:
                    spider_name=pending_job.get('spider')
                    print('pending spider:'+str(spider_name))
        except Exception as e:
            print(e)


def get_pending_spider(addr_data):
    addr = addr_data[0]
    name = addr_data[1]
    url='http://%s:6800/jobs' % addr
    res = requests.get(url)
    print(20 * "-" + name+' url:%s'%url+ 20 * '-')
    try:
        raw_html=etree.HTML(res.text)
        for detail in raw_html.xpath('/html/body/table/tr')[2:]:
            if detail.xpath('th'):
                print('pending end!')
                break
            else:
                pro=detail.xpath('td[1]/text()')
                spider = detail.xpath('td[2]/text()')
                print(pro)
                print(spider)


    except Exception as e:
        print(e)

if __name__ == '__main__':
    server_dict = {
      #
    }
    for _ in range(5):
        for addr_data in server_dict.items():
            get_scrapyd_list(addr_data)
            # get_pending_spider(addr_data)
        print(80*'*'+'\n')
        time.sleep(3)