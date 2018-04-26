#coding:utf8

import tensorflow as ten
import numpy as num
import matplotlib.pyplot as plt

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


def conv2_test():
    x=ten.constant([1,2,3,4,5,6,7,8,9],shape=[1,3,3,1],dtype=ten.float32)
    filter=ten.constant([1,2,3,4],shape=[2,2,1,1],dtype=ten.float32)
    op1 = ten.nn.conv2d(x,filter,strides=[1, 1, 1, 1],padding='SAME')
    op2 = ten.nn.conv2d(x,filter,strides = [1, 1, 1, 1],padding = 'VALID')
    with ten.Session() as se:
        result1 = se.run([op1])
        result2 = se.run([op2])
        print(result1)
        print(result2)
        # print(ten.convert_to_tensor(result))

#产生一个正态分布
def show_truncated():
    ten.InteractiveSession()
    s=ten.truncated_normal(shape=[20,20],mean=0,stddev=1)
    plt.plot(s.eval(),'b.')
    plt.show()

if __name__ == '__main__':
    #se=ten.Session()
    # se=ten.InteractiveSession()
    # x,y=input_data()
    #result=se.run(cacul(x,y))
    # x.initializer.run()
    # result=sub_cacul(x,y).eval()
    # print(result)
    #se.close()
    # conv2_test()
    show_truncated()
