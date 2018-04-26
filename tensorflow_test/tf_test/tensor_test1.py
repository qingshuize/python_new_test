#coding:utf8
import tensorflow as tf
import numpy as np
LOG_PATH='/Users/qmp/Desktop/graphs'

x = np.random.rand(100).astype("float32")

def tensor_board():
    learning_rate=0.6
    with tf.variable_scope('y'):
        y=2.5*x+0.8
        tf.summary.histogram("method_demo"+"/y",y) #可视化观看变量y

    with tf.variable_scope('w'):
        w=tf.Variable(tf.random_uniform([1],-100.0,100.0))
        tf.summary.histogram("method_demo" + "/w", w)

    with tf.variable_scope('b'):
        b=tf.Variable(tf.zeros([1]))
        tf.summary.histogram("method_demo" + "/b", b)


    with tf.name_scope('Y'):
        Y = w * x + b #sigmoid神经元
        tf.summary.histogram("method_demo"+"/Y",Y)#可视化观看变量

    # 最小化均方
    with tf.name_scope('loss'):
        loss = tf.reduce_mean(tf.square(Y - y))
        tf.summary.histogram("method_demo"+"/loss",loss) #可视化观看变量
        tf.summary.scalar("method_demo"+'loss',loss) #可视化观看常量

    # 定义学习率，我们先使用0.7来看看效果
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    with tf.name_scope('train'):
        train = optimizer.minimize(loss)

    init = tf.initialize_all_variables()
    sess = tf.Session()
    sess.run(init)
    #合并到Summary中
    merged = tf.summary.merge_all()
    #选定可视化存储目录
    writer = tf.summary.FileWriter(LOG_PATH,sess.graph)

    for step in xrange(500):
        sess.run(train)
        if step % 5 == 0:
            print(step, "w:",sess.run(w),"b:", sess.run(b))
            result = sess.run(merged)  # merged也是需要run的
            writer.add_summary(result, step)  # result是summary类型的


from matplotlib import pyplot as plt
def line_test():
    learning_rate=0.1
    x_data=np.random.random_sample(100)
    y_data=4.2*x_data+2.5

    #线性模型
    W=tf.Variable(0.)
    b=tf.Variable(0.)
    y=W*x_data+b

    loss=tf.reduce_mean(tf.square(y-y_data))
    optimizer=tf.train.GradientDescentOptimizer(learning_rate)

    # 训练的目的就是最小化代价函数，用minimize
    train=optimizer.minimize(loss)
    init=tf.initialize_all_variables()
    with tf.Session() as se:
        se.run(init)
        for i in range(500):    #迭代500次
            se.run(train)

            if i%5==0:  #以5为步长打印
                print(i,se.run([W,b]))
        plt.plot(x_data,y_data,'r.',label='raw data')
        plt.show()



if __name__ == '__main__':
    tensor_board()
    # line_test()


