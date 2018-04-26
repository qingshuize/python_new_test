#coding:utf8
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

#定义权重变量
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)    #产生一个正态分布
    return tf.Variable(initial)

#定义偏移量变量
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


#2维卷积函数
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1],
                        padding='SAME')

'''
#使用最大池化函数max_pool_2x2对卷积的输出结果进行池化操作
#tf.nn.max_pool是TensorFlow中的最大池化函数，我们使用2x2的最大池化，即将一个2x2的像素块降为1x1的像素。最大池化会保留原始像素块中灰度值最高的那一个像素，即保留最显著的特征。
#因为希望整体缩小图片尺寸，因此池化层的strides也设为横竖两个方向以2为步长。如果步长还是1，那么我们会得到一个尺寸不变的图片。
'''

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1],
                          padding='SAME')




if __name__ == '__main__':
    mnist = input_data.read_data_sets("mnist/", one_hot=True)
    sess = tf.InteractiveSession()

    x = tf.placeholder(tf.float32, [None, 784])
    y_ = tf.placeholder(tf.float32, [None, 10])
    x_image = tf.reshape(x, [-1, 28, 28, 1])

    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])

    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    W_conv2 = weight_variable([5, 5, 32, 64])  # 32是32个特征
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat
                                 , W_fc1) + b_fc1)

    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
    # cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv),reduction_indices=[1]))

    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=tf.matmul(h_fc1_drop, W_fc2) + b_fc2))
    train_step = tf.train.AdamOptimizer(2e-3).minimize(cost)    #使用Adam优化器

    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    tf.global_variables_initializer().run()

    for i in range(11000):
        batch = mnist.train.next_batch(50)
        train_step.run(feed_dict={x: batch[0], y_: batch[1],
                                  keep_prob: 0.5})
        if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict={x: batch[0],
                                                      y_: batch[1],
                                                      keep_prob: 1.0})
            #开始训练过程。首先依然是初始化所有参数，设置训练时Dropout的Keep_prob比率为0.5。然后使用大小为50的mini-batch，共进行10000次训练迭代，参与训练的样本数量总人为50万。
#其中每100次训练，我们会对准确率进行一次评测（评测时keep_prob设为1），用以实时监测模型的性能。

            print("step %d ,train_accuracy %g" % (i, train_accuracy))


    print("test accuray %g" % accuracy.eval({x: mnist.test.images,
                                             y_: mnist.test.labels, keep_prob: 1.0}))