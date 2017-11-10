#coding:utf-8
import tensorflow as ten
import numpy as num
from tensorflow.examples.tutorials.mnist import input_data
path='/Users/qmp/Desktop/'
''''
mnist=input_data.read_data_sets(path+'MNIST_data/',one_hot=True)

print(mnist.train.images.shape,mnist.train.labels.shape)    #采集样本大小
print(mnist.test.images.shape,mnist.test.labels.shape)
print(mnist.validation.images.shape,mnist.validation.labels.shape)
'''
x=ten.constant([1,2,4,1,5,6],shape=[2,3])
y=ten.constant([0,2,3,9,3,2],shape=[3,2])
z=ten.matmul(x,y)
sess=ten.Session(config=ten.ConfigProto(log_device_placement=True))
sess.run(z)