#!/usr/bin/env python

# !/usr/bin/env python
# coding: utf-8

"""
    __title__ = 'selenium Chrome'
    __author__ = 'qmp'
    __mtime__ = '2018/8/21'

    # code is far away from bugs with the god animal protecting
    Stay Hungry,Stay Foolish.

   	______	______
	______	______
	______


"""

from selenium import webdriver
import time
import commands
import random


def Browser_get(s_type, words):
	# s=webdriver.Safari()
	d = webdriver.Chrome()
	try:
		if s_type == 's':
			url = 'https://www.sogou.com/'
			search_id = 'query'
			search_btn = 'stb'
		elif s_type == 'b':
			url = 'https://www.baidu.com'
			search_id = 'kw'
			search_btn = 'su'
		elif s_type == 'w':
			url = 'https://www.wikipedia.org'
			search_id = 'searchInput'
			search_btn = 'pure-button pure-button-primary-progressive'
		else:
			url = 'https://www.google.com/'
			search_id = 'lst-ib'
			search_btn = 'btnK'
		
		# if GET_url_info(url):
		if GET_url_info(url):
			print('ok!')
		else:
			print('url can not reach!!!')
		d.get(url)
		d.implicitly_wait(10)
		d.find_element_by_id(search_id).send_keys(words)
		d.find_element_by_id(search_btn).click() if s_type == 's' else d.find_element_by_name(
			search_btn).click() if s_type == 'g' else None
	
	
	except:
		pass
	finally:
		time.sleep(6)
		# d.quit()
		d.close()
	# print(d)


def GET_url_info(url):
	# url = 'https://www.baidu.com'
	print(url)
	s = commands.getstatusoutput('curl %s -m 5' % url)
	print('status >>> ', s[0])
	return False if s[0] else True


if __name__ == '__main__':
	s_type = ['b', 's']
	for i in range(3):
		Browser_get(random.choice(s_type), u'埃尔南德斯')