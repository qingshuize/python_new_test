#!/usr/bin/env python
# coding: utf-8

"""
    __title__ = ''
    __author__ = 'qmp'
    __mtime__ = '2018/10/11'
    
    # code is far away from bugs with the god animal protecting
    Stay Hungry,Stay Foolish.
   	
   	______	______
	______	______
	______


"""
import pandas as pd
import os
import csv
from pyecharts import TreeMap


def Write_csv(name,data,filename):
	# 建立DataFrame对象
	p = pd.DataFrame(columns=name, data=data)
	# data write
	p.to_csv(filename, encoding='utf8', index=False)
	print('write data ok!')


def Pandas_write_file(list_info,filename):
	try:
		name=['john','peter','tim','victor']
		if not os.path.exists(filename):
			Write_csv(name,list_info,filename)
		else:
			size=os.path.getsize(filename)
			if not size:
				print('size>>>>>%s'%size)
				Write_csv(name, list_info, filename)
			else:
				## 追加到文件后面
				with open(filename,'a+') as f:
					writer=csv.writer(f)
					writer.writerows(list_info)
				print('add data ok!')
	except Exception as e:
		print(e)

def Pandas_read_file(filename):
	with open(filename,'r') as f:
		reader = csv.reader(f)
		data=[]
		for row in reader:
			data.append(row)
	print(data)

if __name__ == '__main__':
	# PATH='/Users/qmp/Desktop/'
	PATH='./'
	list_info=[['12','23','20','18'],['21','20','24','19']]
	# Pandas_write_file(list_info,PATH+'pd_test.csv')
	Pandas_read_file(PATH+'pd_test.csv')