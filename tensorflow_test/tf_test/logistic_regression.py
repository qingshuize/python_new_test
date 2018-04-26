#coding:utf8

##逻辑回归
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import time
#学习速率
starter_learning_rate = 1e-1
batch_size = 128
n_epochs = 10


def main():
    mnist=input_data.read_data_sets('data/mnist',one_hot=True)
    print('训练集大小：'+str(mnist.train.images.shape))
    print('测试集大小：'+str(mnist.test.images.shape))
    print('验证集大小：'+str(mnist.validation.images.shape))
    sess=tf.InteractiveSession()
    ##28*28像素图案
    x=tf.placeholder(tf.float32,[None,784])
    #初始化全为0，one-hot编码是10维向量
    w=tf.Variable(tf.zeros([784,n_epochs]))
    b=tf.Variable(tf.zeros([n_epochs]))

    logits = tf.matmul(x, w) + b

    y=tf.placeholder(tf.float32,[None,n_epochs])

    ##损失函数

    ##tf.nn.softmax_cross_entropy_with_logits损失函数集成了以下的步骤
    cost=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=logits))

    # ##step1: softmax处理
    preds = tf.nn.softmax(logits)
    # ##step2: cross_entropy（交叉熵函数）处理
    # cost=tf.reduce_mean(-tf.reduce_sum(y*tf.log(preds),reduction_indices=[1]))





    ##自适应学习速率;初始的学习速率是0.1，每经过10万轮次训练后，学习速率变为原来的0.98
    global_step = tf.Variable(0, trainable=False)
    decayed_learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step, 100, 0.98, staircase=True)

    ##随机梯度下降优化器
    optimizer = tf.train.GradientDescentOptimizer(decayed_learning_rate).minimize(cost,global_step=global_step)
    tf.global_variables_initializer().run()


    ##训练数据
    for _ in range(20000):  #迭代执行训练操做
        batch_xs,batch_ys=mnist.train.next_batch(batch_size)
        optimizer.run({x:batch_xs,y:batch_ys})

    ##验证模型准确率
    correct_pred=tf.equal(tf.argmax(preds,1),tf.argmax(y,1))
    accuracy=tf.reduce_mean(tf.cast(correct_pred,tf.float32))

    print(accuracy.eval({x:mnist.test.images,y:mnist.test.labels}))


if __name__ == '__main__':
    main()