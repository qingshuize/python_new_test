# coding:utf8
import sys

sys.path.append("/Users/qmp/Desktop/python_new_test_bak")
import datetime
import ast
import time
import xlrd, xlwt
from utils.db_config import *


def get_search_data(s_day, e_day, s_type):
	# 搜索热度
	if s_type == 's':
		sql = 'select words,count(1) as num,(select mf_jigou_info.id from mf_jigou_info where name=words and display_flag=1 limit 1) as i,(select mf_product_company.id from mf_product_company where product=words and display_flag=1 limit 1) as o,(select mf_person_info.id from mf_person_info where name=words and display_flag=1 limit 1) as p from search_magic_history where create_time between ""%s" 00:00:00" and ""%s" 23:59:59"   GROUP BY words order by num desc'
	# 人物
	elif s_type == 'p':
		sql = 'SELECT keywords,count(1) as num FROM mf_count_ip WHERE visit_time between ""%s" 00:00:00" and ""%s" 23:59:59" AND domain IN ("ios1.api.qimingpian.com","vip.api.qimingpian.com","pro.api.qimingpian.com","wx.api.qimingpian.com","az.qpi.qimingpian.com") AND ( keywords <> "" AND keywords <> "0|" AND keywords not like "%%%%|"  ) AND method = "person" GROUP BY keywords ORDER BY num desc'
	# 项目
	elif s_type == 'i':
		sql = 'SELECT `keywords`,count(1) as num,mf_product_company.id FROM mf_count_ip join mf_product_company WHERE product=SUBSTRING_INDEX(keywords,"|",-1) and visit_time between ""%s" 00:00:00" and ""%s" 23:59:59" AND `method` IN ("c1","c3") AND `keywords` <> "" AND keywords not like "%%|" AND `domain` IN ("vip.api.qimingpian.com","ios1.api.qimingpian.com","pro.api.qimingpian.com","wx.api.qimingpian.com","az.api.qimingpian.com") GROUP BY keywords ORDER BY num desc'
	# 机构
	elif s_type == 'o':
		sql = 'SELECT `keywords`,count(1) as num,mf_jigou_info.id  FROM mf_count_ip join mf_jigou_info WHERE mf_jigou_info.name=keywords and visit_time between ""%s" 00:00:00" and ""%s" 23:59:59" AND `method` = "jigou3info" AND ( `keywords` <> "汉富资本" AND `keywords` <> "百场汇" AND `keywords` <> "") AND `domain` IN ("vip.api.qimingpian.com","ios1.api.qimingpian.com","pro.api.qimingpian.com","wx.api.qimingpian.com","az.api.qimingpian.com") GROUP BY keywords ORDER BY num desc'
	else:
		sql = ''
	# res=1
	# while res:
	if s_day != e_day:
		sql = sql + ' limit 5000'
	cur = db.execute_sql(sql, [s_day, e_day])
	# i+=2000
	res = cur.fetchall()
	print('get data ok!')
	db.close()
	yield res


def read_excel(date):
	try:
		xlsfile = '/Users/qmp/Desktop/list_data_%s.xlsx' % date
		book = xlrd.open_workbook(xlsfile)  # 得到Excel文件的book对象，实例化对象
		sheet_name_list = book.sheet_names()  # 获得指定索引的sheet表名字
		for name in sheet_name_list:
			if name.encode('utf8').startswith(date):
				print(name)
				sheet1 = book.sheet_by_name(name)  # 通过sheet名字来获取，当然如果知道sheet名字就可以直接指定
				nrows = sheet1.nrows  # 获取行总数
				print("rows:" + str(nrows))
				# 循环打印每一行的内容
				s = []
				for i in range(nrows):
					d = {}
					d[sheet1.row_values(i)[0]] = sheet1.row_values(i)[1]
					s.append(d)
				with open('/Users/qmp/Desktop/hbase_data/list_data_%s.json' % date, 'w') as f:
					f.write(str(s))
				print('save json ok!')
	except Exception as e:
		print(e)


def select_product():
	sql = 'select product from mf_product_company group by product'
	cusor = ti_db.execute_sql(sql)
	res = cusor.fetchall()
	pro_list = map(lambda x: x[0], res)
	return pro_list


def query_data(s_date, e_date):
	i = 0
	# res=1
	# while res:
	sql = 'select keywords,count(*) as num from mf_count_ip_hz where method = "wdproduct"  and keywords not in (select company from mf_product_company group by company) and visit_time BETWEEN "%s 00:00:00" AND "%s 23:59:59" GROUP BY keywords ORDER BY num desc limit %s,5000' % (
		s_date, e_date, i)
	print(sql)
	# i+=3000
	cusor1 = ti_db.execute_sql(sql)
	res = cusor1.fetchall()
	yield res
	
	ti_db.close()


def get_hz_ip_data(s_date, e_date):
	workbook = xlwt.Workbook(encoding='utf-8')
	date = ''.join(s_date.split('-')) if s_date == e_date else ''.join(s_date.split('-')) + '_' + ''.join(
		e_date.split('-'))
	worksheet = workbook.add_sheet('%s 数据统计' % date)
	i = 0
	try:
		for info in query_data(s_date, e_date):
			for s in info:
				if len(s[0]) > 1 and s[0] not in product_list:
					worksheet.write(i, 0, label=s[0])
					worksheet.write(i, 1, label=s[1])
					i += 1
					# else:
					# print(s[0],len(s[0]))
		print('write ok!')
	except Exception as e:
		print(e)
	print('total number:', str(i))
	workbook.save('/Users/qmp/Desktop/list_data_%s.xlsx' % date)
	print('excel data save success!!')
	read_excel(date)


def select_max():
	sql = 'select max(id) from search_hot_key_history'
	res = URL_db.execute_sql(sql)
	info = res.fetchone()[0]
	return info if info else 0


def update_display(date):
	update_sql = 'update search_hot_key_history set display_flag=0 where date_time="%s"'
	URL_db.execute_sql(update_sql, [date])
	print('change status ok!')


def insert_data(date, words, n):
	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	add_sql = 'insert into search_hot_key_history(date_time,keyword,search_num,sort,create_time,update_time) value(%s,%s,%s,%s,%s,%s)'
	URL_db.execute_sql(add_sql, [date, words, n, select_max(), now, now])
	print('add ok!')


def demo_test(date):
	print(date)
	sql = 'select words,count(1) as num from search_magic_history where create_time regexp "%s" and external_flag!=0 GROUP BY words order by num desc limit 10' % date
	cusor = URL_db.execute_sql(sql)
	result = cusor.fetchall()
	if result:
		for x in result:
			words = x[0]
			n = x[1]
			print(words, n)
			select_sql = 'select count(1) from search_hot_key_history where date_time=%s' % date
			cusor0 = URL_db.execute_sql(select_sql)
			if cusor0.fetchone()[0] == 10:
				update_display(date)
				print('is exist!!')
			insert_data(date, words, n)


def select_id_func(word, s_type):
	if s_type == 'o':
		sql = 'select id from mf_jigou_info where name=%s limit 1'
	elif s_type == 'i':
		sql = 'select id from mf_person_info where name=%s limit 1'
	else:
		sql = 'select id from mf_product_company where product=%s limit 1'
	cusor = ti_db.execute_sql(sql, [word])
	res = cusor.fetchone()[0]
	return res


if __name__ == '__main__':
	path = '/Users/qmp/Desktop/hbase_data/'
	now_day = datetime.date.today()
	# 昨天的记录
	# demo_test(str(now_day - datetime.timedelta(1)))
	# day_1_raw=now_day - datetime.timedelta(0)
	# day_1 = str(day_1_raw)
	##range(15, 0, -1)
	raw_day_1 = datetime.date(2018, 8, 5)
	day_1 = str(raw_day_1)
	
	# product_list = select_product()
	for i in [0]:
		before_day = str(raw_day_1 - datetime.timedelta(i))
		print(before_day)
		for s_type in ['i', 'o', 'p', 's']:
			time.sleep(1)
			dd = []
			for raw_data in get_search_data(before_day, day_1, s_type):
				for x in raw_data:
					ss = {}
					if s_type == 's':
						t_type, s_id = ('i', x[2]) if x[2] else ('o', x[3]) if x[3] else ('p', x[4]) if x[4] else (
						None, None)
						if not t_type:
							continue
						ss['s_type'] = t_type
						ss['id'] = s_id
					if s_type not in ['c', 's']:
						ss['id'] = int(x[2]) if s_type in ['i', 'o'] else int(x[0].split('|')[0])
					ss['keywords'] = x[0]
					ss['num'] = int(x[1])
					dd.append(ss)
			print(len(dd))
			if s_type == 'i':
				base_name = 'item_data_'
			elif s_type == 'o':
				base_name = 'org_data_'
			elif s_type == 'p':
				base_name = 'person_data_'
			else:
				base_name = 'HBASE_data_'
			date = ''.join(before_day.split('-')) if before_day == day_1 else ''.join(
				before_day.split('-')) + '_' + ''.join(day_1.split('-'))
			file_name = base_name + date + '.json'
			# if not os.path.exists(path+file_name):
			with open(path + file_name, 'w') as f:
				f.write(str(dd))
			print('%s write ok!' % file_name)
			
			# get_hz_ip_data(before_day, before_day)
			# get_hz_ip_data(before_day,str(now_day))
			
			# with open(path + 'HBASE_data_201806.json', 'r') as f:
			#     data=f.read()
			# # print(data)
			# cc = []
			# for x in json.loads(data):
			#     ss = {}
			#     ss[x.keys()[0]] = str(x.values()[0])
			#     cc.append(ss)
			# with open(path + 'HBASE_data_20180612.json', 'w') as f:
			#     f.write(str(cc))
			# print('write ok!')
			# print(type(ast.literal_eval(data)))
			# print(type(json.loads(str(data))))
			# print(type(data))
			# s=eval(data)
			# print(s)
