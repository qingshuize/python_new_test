#coding:utf8
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
    x=tf.placeholder(dtype=tf.float32,shape=[None,784],name='x')
    #初始化全为0，one-hot编码是10维向量
    w=tf.Variable(tf.zeros([784,n_epochs]))
    b=tf.Variable(tf.zeros([n_epochs]))

    logits = tf.matmul(x, w) + b

    preds = tf.nn.softmax(logits)
    y=tf.placeholder(dtype=tf.float32,shape=[None,n_epochs],name='y')

    ##损失函数
    cross_entropy=tf.reduce_mean(-tf.reduce_sum(y*tf.log(preds),reduction_indices=[1]))

    ##随机梯度下降SGD

    ##自适应学习速率;初始的学习速率是0.1，每经过10万轮次训练后，学习速率变为原来的0.98
    global_step = tf.Variable(0, trainable=False)
    decayed_learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step, 100000, 0.98, staircase=True)
    optimizer = tf.train.GradientDescentOptimizer(decayed_learning_rate).minimize(cross_entropy)

    tf.global_variables_initializer().run()

    ##训练数据
    for _ in range(20000):
        batch_xs,batch_ys=mnist.train.next_batch(batch_size)
        optimizer.run({x:batch_xs,y:batch_ys})

    ##验证模型准确率
    correct_pred=tf.equal(tf.argmax(preds,1),tf.argmax(y,1))
    accuracy=tf.reduce_mean(tf.cast(correct_pred,tf.float32))

    print(accuracy.eval({x:mnist.test.images,y:mnist.test.labels}))


    # correct_preds = tf.equal(tf.argmax(preds, 1), tf.argmax(y, 1))
    # accuracy = tf.reduce_sum(tf.cast(correct_preds, tf.float32), axis=0)
    #
    # with tf.Session() as sess:
    #     writer = tf.summary.FileWriter('./logistic_log', sess.graph)
    #     start_time = time.time()
    #     sess.run(tf.global_variables_initializer())
    #     n_batches = int(mnist.train.num_examples / batch_size)
    #     for i in range(n_epochs):  # train the model n_epochs times
    #         total_loss = 0
    #         for _ in range(n_batches):
    #             X_batch, Y_batch = mnist.train.next_batch(batch_size)
    #             _, loss_batch = sess.run(
    #                 [optimizer, loss], feed_dict={x: X_batch,
    #                                               y: Y_batch})
    #             total_loss += loss_batch
    #         print('Average loss epoch {0}: {1}'.format(i, total_loss / n_batches))
    #
    #     print('Total time: {0} seconds'.format(time.time() - start_time))
    #
    #     print('Optimization Finished!')  # should be around 0.35 after 25 epochs
    #
    #     # test the model
    #     n_batches = int(mnist.test.num_examples / batch_size)
    #     total_correct_preds = 0
    #
    #     for i in range(n_batches):
    #         X_batch, Y_batch = mnist.test.next_batch(batch_size)
    #         accuracy_batch = sess.run(accuracy, feed_dict={x: X_batch, y: Y_batch})
    #         total_correct_preds += accuracy_batch
    #
    #     print('Accuracy {0}'.format(total_correct_preds / mnist.test.num_examples))

if __name__ == '__main__':
    main()