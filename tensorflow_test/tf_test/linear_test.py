#coding:utf8
import tensorflow as tf
import numpy as np
import xlrd
path='/Users/qmp/Desktop/'

data_file=path+''
book = xlrd.open_workbook(data_file, encoding_override='utf-8')
sheet = book.sheet_by_index(0)
data = np.asarray(
    [sheet.row_values(i) for i in range(1, sheet.nrows)], dtype=np.float32)
n_samples = sheet.nrows - 1

#误差函数处理
def huber_loss(labels, predictions, delta=1.0):
    residual = tf.abs(predictions - labels)
    condition = tf.less(residual, delta)
    small_res = 0.5 * residual**2
    large_res = delta * residual - 0.5 * delta**2
    return tf.where(condition, small_res, large_res)

#线性关系Y=aX+b
def main():
    X=tf.placeholder(tf.float64,shape=[],name='x')
    Y=tf.placeholder(tf.float64,shape=[],name='y')
    a=tf.get_variable(name='a',shape=[],dtype=tf.int64,initializer=tf.truncated_normal_initializer())
    b=tf.get_variable(name='b',shape=[],dtype=tf.int64,initializer=tf.truncated_normal_initializer())

    #输出函数
    Y_func=a*X+b

    #误差函数(梯度下降)
    loss=tf.square(Y-Y_func,name='loss')

    #优化函数,学习率
    optizmer=tf.train.GradientDescentOptimizer(learning_rate=1e-4).minimize(loss)

    #参数设置tf.Variabel(trainable=False)就表示不对该参数进行更新，默认True

    init=tf.global_variables_initializer()
    h_loss=huber_loss
    with tf.Session() as se:
        writer=tf.summary.FileWriter(path+'linear_log',graph=se.graph)
        se.run(init)
        for _ in range(20):
            total_loss=0
            for x,y in data:
                _,l=se.run([optizmer,h_loss],{X:x,Y:y})
                total_loss += l
            print("Epoch {0}: {1}".format(i, total_loss / n_samples))



if __name__ == '__main__':
    main()