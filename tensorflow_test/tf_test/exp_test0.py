#coding:utf8

import tensorflow as ten
import numpy as num

def input_data():
    #ten.constant()     ---张量：常量值
    #x=ten.constant(num.float64(num.random.rand(1,100))) #random.rand() 简单随机值
    #x=ten.constant(num.int32(num.random.randint(1,10,[1,3])))
    #print('x:',x)
    #y=ten.constant(num.int32(num.random.randint(2,5,[3,1])))
    #y=ten.constant(num.float64(num.random.randn(100,1)))    #random.randn() 正态分布抽样
    z=ten.Variable(num.int32(num.random.randint(3,10,[2,3])))
    w=ten.constant(num.int32(num.random.randint(3,10,[2,3])))
    #print('y:',y)
    return z,w
def cacul(x,y):
    pro=ten.matmul(x,y)
    return pro

def sub_cacul(x,y):
    pro=ten.subtract(x,y)
    return pro

if __name__ == '__main__':
    #se=ten.Session()
    se=ten.InteractiveSession()
    x,y=input_data()
    #result=se.run(cacul(x,y))
    x.initializer.run()
    result=sub_cacul(x,y).eval()
    print(result)
    #se.close()
