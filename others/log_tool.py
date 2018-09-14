#!/usr/bin/env python
# coding: utf-8

"""
    __title__ = ''
    __author__ = 'qmp'
    __mtime__ = '2018/9/14'
    
    # code is far away from bugs with the god animal protecting
    Stay Hungry,Stay Foolish.
   	
   	______	______
	______	______
	______


"""
import logging

logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


def try_error(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as e:
            logging.error('*****出错啦!!*****')
            logging.error(e)
    
    return wrapper
