#!/usr/bin/env python
# coding: utf-8

"""
    __title__ = 'redis mongodb '
    __author__ = 'xxx'
    __mtime__ = '2018/9/14'
    
    # code is far away from bugs with the god animal protecting
    Stay Hungry,Stay Foolish.
   	
   	______	______
	______	______
	______


"""
from log_tool import *
from pymongo import MongoClient
import redis


def Redis_handle():
    #r=redis.StrictRedis(host='127.0.0.1',port=6379)
    r=redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)

    print(r.lrange('list_test',1,20))
    for i in ['q','w','e','r']:
        # r.rpush('list_test',i)

        r.lpop('list_test')
    print(r.lrange('list_test', 1, 20))
    # pipe = r.pipeline(transaction=True)
    # name=r.get('name')
    # print(type(eval(name)))
    # print(name)
    # r.set('age',29)
    # print(type(eval(r.get('age'))))
    # time.sleep(2)
    # pipe.execute()


    #事务
    # try:
    #     # pipe.watch('a')
    #     pipe.multi()
    #     pipe.set('here', 'there')
    #     pipe.set('here1', 'there1')
    #     pipe.set('here2', 'there2')
    #     time.sleep(5)
    #     pipe.execute()
    #
    # except redis.exceptions.WatchError as e:
    #     print("Error")
	
	
	
class Mongo_handle(object):
	
	def __init__(self, dbs='info', set='raw_data', name='test'):
		local_ip = '127.0.0.1'
		# self.conn = MongoClient(host=data_ip, port=27017,connect=False)
		
		self.conn = MongoClient("mongodb://root:xxx@%s/admin" % local_ip)
		db = self.conn[dbs]  # 连接mydb数据库，没有则自动创建
		self.my_set = db[set][name]
	
	# db = MongoClient(host=data_ip, port=27017, username='root', password='qmp').cc
	# self.my_set = db[set][name]
	
	# try:
	# 	self.conn.database_names()
	# except:
	# 	# 认证用户密码
	# 	admin_db = self.conn.admin
	# 	admin_db.authenticate('root','xxx')
	# finally:
	# 	logging.debug('auth dbs success!!')
	# 	db = self.conn[dbs]  # 连接mydb数据库，没有则自动创建
	# 	self.my_set = db[set][name]	# 使用test_set集合，没有则自动创建
	#
	@try_error
	def get_total_numbers(self):
		return self.my_set.find().count()
	
	@try_error
	def select_data(self, query, sort_item):
		# 查询全部
		for i in self.my_set.find(query):
			print(i)
		
		# 对sort_item字段进行排序
		result = self.my_set.find(query).sort(sort_item)
		logging.debug('get data ok!')
		return result
	
	@try_error
	def insert_data(self, data):
		self.my_set.insert(data)
		logging.debug('add data ok!')
	
	@try_error
	def add_data(self, data):
		# 若新增数据的主键已经存在，则会对当前已经存在的数据进行修改操作（单个文档）
		self.my_set.save(data)
		logging.debug('add data ok!')
	
	@try_error
	def update_data(self, query, newvalues):
		# 按照query匹配条件，替换旧值为newvalues
		# 例如
		# query = { "xxx": { "$regex": "^A" } }
		# newvalues = { "$set": { "xxx": "xx" } }
		self.my_set.update_many(query, newvalues)
		logging.debug('update data ok!')
	
	@try_error
	def delete_all_data(self, query={}):
		self.my_set.delete_many(query)
		logging.debug('delete all data!')
	
	@try_error
	def close_conn(self):
		self.conn.close()
