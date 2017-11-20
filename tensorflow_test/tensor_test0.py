#coding:utf-8
import tensorflow as ten
import numpy as num
import random
from tensorflow.examples.tutorials.mnist import input_data
path='/Users/qmp/Desktop/'
''''
mnist=inumut_data.read_data_sets(path+'MNIST_data/',one_hot=True)

print(mnist.train.images.shape,mnist.train.labels.shape)    #采集样本大小
print(mnist.test.images.shape,mnist.test.labels.shape)
print(mnist.validation.images.shape,mnist.validation.labels.shape)
'''
def test():
    x=ten.constant([1,2,4,1,5,6],shape=[2,3])
    y=ten.constant([0,2,3,9,3,2],shape=[3,2])
    z=ten.matmul(x,y)
    sess=ten.Session(config=ten.ConfigProto(log_device_placement=True))
    sess.run(z)

def maxmatix(x):
    s=x.shape
    if s>1:
        tmp = num.max(x,axis=1)
        x -= tmp
        x = num.exp(x)
        x /= num.sum(x,axis=1)
    else:
        tmp = num.max(x)
        x -= tmp
        x = num.exp(x)
        x /= num.sum(x)
    return x


def gradcheck_naive(f, x):
    rndstate = random.getstate()
    random.setstate(rndstate)
    fx, grad = f(x)  # fx=num.sum(x ** 2), grad=x * 2
    h = 1e-4


    it = num.nditer(x, flags=['multi_index'], op_flags=['readwrite'])

    while not it.finished:
        ix = it.multi_index  # starts from (0, 0) then (0, 1)

        x[ix] += h  # To calculate [f(xi+h)-f(xi-h)] / 2h
        random.setstate(rndstate)
        fxh, _ = f(x)
        x[ix] -= 2 * h
        random.setstate(rndstate)
        fxnh, _ = f(x)
        x[ix] += h
        numgrad = (fxh - fxnh) / 2 / h
        reldiff = abs(numgrad - grad[ix]) / max(1, abs(numgrad), abs(grad[ix]))
        if reldiff > 1e-5:
            print "Gradient check failed."
            print "First gradient error found at index %s" % str(ix)
            print "Your gradient: %f \t Numerical gradient: %f" % (grad[ix], numgrad)
            return

        it.iternext()

    print "Gradient check passed"

def test_py(shape,r):
    ten.InteractiveSession()
    x=ten.truncated_normal(shape,stddev=r)  #stddev:标准差 随机变量，normal分布
    print(x.eval())




def maxtrix_image():
    # 生成0和1矩阵
    v1 = ten.Variable(ten.zeros([3, 3, 3]), name="v1")
    v2 = ten.Variable(ten.ones([10, 5]), name="v2")

    # 填充单值矩阵
    v3 = ten.Variable(ten.fill([2, 3], 9))

    # 常量矩阵
    v4_1 = ten.constant([1, 2, 3, 4, 5, 6, 7])
    v4_2 = ten.constant(-1.0, shape=[2, 3])

    # 生成等差数列
    v6_1 = ten.linspace(10.0, 12.0, 30, name="linspace")  # float32 or float64
    v7_1 = ten.range(10, 20, 3)  # just int32

    # 生成各种随机数据矩阵
    v8_1 = ten.Variable(ten.random_uniform([2, 4], minval=0.0, maxval=2.0, dtype=ten.float32, seed=1234, name="v8_1"))
    v8_2 = ten.Variable(ten.random_normal([2, 3], mean=0.0, stddev=1.0, dtype=ten.float32, seed=1234, name="v8_2"))
    v8_3 = ten.Variable(ten.truncated_normal([2, 3], mean=0.0, stddev=1.0, dtype=ten.float32, seed=1234, name="v8_3"))
    v8_4 = ten.Variable(ten.random_uniform([2, 3], minval=0.0, maxval=1.0, dtype=ten.float32, seed=1234, name="v8_4"))
    v8_5 = ten.random_shuffle([[1, 2, 3], [4, 5, 6], [6, 6, 6]], seed=134, name="v8_5")

    # 初始化
    init_op = ten.initialize_all_variables()

    # 保存变量，也可以指定保存的内容
    saver = ten.train.Saver()
    # saver = ten.train.Saver({"my_v2": v2})

    # 运行
    with ten.Session() as sess:
        sess.run(init_op)
        # 输出形状和值
        print ten.Variable.get_shape(v1)  # shape
        print sess.run(v1)  # vaule

        # numpy保存文件
        num.save("/Users/qmp/Desktop/v1.numy", sess.run(v1))  # numpy save v1 as file
        test_a = num.load("/Users/qmp/Desktop/v1.numy.npy")
        print test_a[1, 2]

        # 一些输出
        print sess.run(v3)

        v5 = ten.zeros_like(sess.run(v1))

        print sess.run(v6_1)

        print sess.run(v7_1)

        print sess.run(v8_5)

        # 保存图的变量
        save_path = saver.save(sess, "/Users/qmp/Desktop/model.ckpt")
        # 加载图的变量
        # saver.restore(sess, "/tmp/model.ckpt")
        print("Model saved in file:",save_path)

if __name__ == '__main__':
    #x=num.matrix('1001,1002,5;3,4,100')
    #print(maxmatix(x))
    #test_py([3,3],1)
    maxtrix_image()
