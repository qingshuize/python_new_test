#coding:utf8
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import time
learning_rate = 1e-3
batch_size = 128
n_epochs = 10


def main():
    mnist=input_data.read_data_sets('data/mnist',one_hot=True)
    x=tf.placeholder(dtype=tf.float64,shape=[None,625],name='x')
    y=tf.placeholder(dtype=tf.float64,shape=[None,10],name='y')
    w=tf.get_variable('weight',shape=(625,10),initializer=tf.truncated_normal_initializer())
    b=tf.get_variable('bias',shape=(10),initializer=tf.zeros_initializer())

    logits = tf.matmul(x, w) + b
    entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=logits)
    loss = tf.reduce_mean(entropy, axis=0)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

    preds = tf.nn.softmax(logits)
    correct_preds = tf.equal(tf.argmax(preds, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_sum(tf.cast(correct_preds, tf.float32), axis=0)

    with tf.Session() as sess:
        writer = tf.summary.FileWriter('./logistic_log', sess.graph)
        start_time = time.time()
        sess.run(tf.global_variables_initializer())
        n_batches = int(mnist.train.num_examples / batch_size)
        for i in range(n_epochs):  # train the model n_epochs times
            total_loss = 0
            for _ in range(n_batches):
                X_batch, Y_batch = mnist.train.next_batch(batch_size)
                _, loss_batch = sess.run(
                    [optimizer, loss], feed_dict={x: X_batch,
                                                  y: Y_batch})
                total_loss += loss_batch
            print('Average loss epoch {0}: {1}'.format(i, total_loss / n_batches))

        print('Total time: {0} seconds'.format(time.time() - start_time))

        print('Optimization Finished!')  # should be around 0.35 after 25 epochs

        # test the model
        n_batches = int(mnist.test.num_examples / batch_size)
        total_correct_preds = 0

        for i in range(n_batches):
            X_batch, Y_batch = mnist.test.next_batch(batch_size)
            accuracy_batch = sess.run(accuracy, feed_dict={x: X_batch, y: Y_batch})
            total_correct_preds += accuracy_batch

        print('Accuracy {0}'.format(total_correct_preds / mnist.test.num_examples))

if __name__ == '__main__':
    main()