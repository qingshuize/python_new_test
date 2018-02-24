# -*- coding: utf-8 -*-

import time
import random
import logging
import traceback

from selenium import webdriver
from scrapy.http import HtmlResponse

from liebao_spider.utils.proxy_ip import IpPooldb
from liebao_spider.utils.proxy_ip import AdslIpPool
from liebao_spider.utils.find_db import FindDB
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from pyvirtualdisplay import Display

##
# Selenium+Phantomjs模拟浏览器
USE_PHANTOMJS = [

]
##
# ADSL拨号获取的代理IP
USE_IPPROXY = [
    # 'crunchbase_project1',
    # 'crunchbase_project2',
    # 'crunchbase_project_detail1',
    # 'crunchbase_project_detail2',
    # 'fellowplus_investor',
    # 'bosszhipin_project',
    # # 'yingjiesheng_jz_project',
    # 'sina_short_url',
    # 'itjuzi_rzdata',
    # 'dongmaiwang_pdf',
    # 'cyzone_investor',
    # 'trjcn_investor',
    # 'xiniudata_hytupu',
    # "crunchbase_rzdata"
]

##
# 免费的代理IP
USE_FREEPROXY = [

]


class LiebaoSpiderProxyMiddleware(object):
    """
    抓取困难的爬虫，采用selenium+phantomjs模拟浏览器
    进行抓取。
    """

    def process_request(self, request, spider):
        if spider.name == "jinritoutiao_news":
            logging.info("*" * 30 + " 正在使用PhantomJS " + "*" * 30)
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.disk-cache"] = True
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")  # 设置user-agent请求头
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            driver.get(request.url)
            for i in xrange(30):
                driver.refresh()
                time.sleep(3)
                body = driver.page_source
                flag = False
                try:
                    s = driver.find_element_by_xpath(
                        '//div[@class="left"]//div[@riot-tag="relatedFeed"]//ul/li[1]/div[@class="item-inner y-box"]'
                        '//a[@class="link title"]')
                    flag = True
                except:
                    pass

                if flag:
                    break
                else:
                    driver.get(request.url)

            url = driver.current_url
            driver.close()
            return HtmlResponse(url, body=body, encoding='utf-8', request=request)

        if spider.name in ["itjuzi_investfirm_manual_step1", "itjuzi_investfirm_manual_step2", "itjuzi_project",
                           "itjuzi_investfirm_manual_step3", "itjuzi_rzdata_list", "itjuzi_project_detail",
                           "itjuzi_project_company_detail"]:

            display = Display(visible=0, size=(800, 600))
            display.start()
            profile = webdriver.FirefoxProfile()
            proxy_ip = AdslIpPool().get_ip().replace('<br>', '')
            if proxy_ip:
                ips = proxy_ip.split(":")
                ip = ips[0]
                port = int(ips[1])
                profile.set_preference("network.proxy.type", 1)
                profile.set_preference('network.proxy.http', ip)
                profile.set_preference('network.proxy.http_port', port)
                profile.set_preference('network.proxy.ssl', ip)
                profile.set_preference('network.proxy.ssl_port', port)
                user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0"
                profile.set_preference("general.useragent.override", user_agent)
                profile.update_preferences()
                binary = FirefoxBinary('/qmp_code/firefox/firefox')

                # driver = webdriver.Firefox(profile)
                driver = webdriver.Firefox(profile, firefox_binary=binary)
                driver.set_window_size(800, 600)
                driver.get(request.url)
                time.sleep(10)
                body = driver.page_source
                print body

                # driver.service.process.send_signal(driver.SIGTERM)

                driver.close()
                display.stop()

                return HtmlResponse(request.url, body=body, encoding='utf-8', request=request)

        if spider.name in USE_PHANTOMJS:
            logging.info("*" * 30 + " 正在使用PhantomJS " + "*" * 30)
            driver = webdriver.PhantomJS()
            driver.get(request.url)
            driver.refresh()
            driver.get(request.url)
            body = driver.page_source
            url = driver.current_url
            driver.close()
            return HtmlResponse(url, body=body, encoding='utf-8', request=request)

        if spider.name in USE_IPPROXY:
            for i in range(10):
                try:
                    logging.info("*" * 30 + " 尝试使用代理IP " + "*" * 30)
                    self.adsl_proxy = AdslIpPool().get_ip().replace('<br>', '')
                    if self.adsl_proxy:
                        request.meta['proxy'] = 'http://' + self.adsl_proxy
                        spider.proxy = self.adsl_proxy
                        logging.info("已获取代理IP, 正在访问..." + request.meta['proxy'])
                        break
                    else:
                        time.sleep(1)
                except Exception, e:
                    self.adsl_proxy = ''
                    logging.error('Error:%s' % e)


class LiebaoSpiderProxyFailMiddleware(object):
    """
    代理IP出错的处理
    """

    def process_exception(self, request, exception, spider):
        try:
            logging.error('代理IP访问失败,spider.name' + spider.name)
            logging.error('代理IP访问失败,spider.proxy' + spider.proxy)
            logging.error('代理IP访问失败,request.url' + request.url)
            logging.error('代理IP访问失败,exception' + exception)

            FindDB().add_error_request(request.url, spider.name, spider.proxy, exception, 'proxy')

            return None
        except:
            logging.error('代理IP访问失败,spider.name' + spider.name)


class FreeProxyMiddleware(object):
    """
    通过抓取的免费代理IP进行访问,暂不使用
    """

    def process_request(self, request, spider):

        if spider.name in USE_FREEPROXY:
            try:
                logging.info("*" * 30 + " 尝试使用代理IP " + "*" * 30)

                self.proxy = IpPooldb().get_valid_ips(10)
                request.meta['proxy'] = 'http://' + \
                                        self.proxy[random.randint(0, len(self.proxy) - 1)]
                logging.info("已获取代理IP, 正在访问..." + request.meta['proxy'])
            except Exception, e:
                traceback.print_exc()
