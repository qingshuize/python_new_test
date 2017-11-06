#coding:utf8
import tensorflow as ten
import numpy as num
def func():
    a=ten.Variable(0,name='s')
    b=ten.constant(2)
    value=ten.add(a,b)
    update=ten.assign(a,value)

    init_op=ten.initialize_all_variables()
    with ten.Session() as se:
        se.run(init_op)
        for _ in range(5):
            result=se.run(update)
            print(result)
def func1():
    x=ten.placeholder(ten.float16)
    y=ten.placeholder(ten.float16)
    output=ten.add(x,y)
    with ten.Session() as se:
        a=se.run([output], feed_dict={x:[num.random.random(1)],y:[num.random.random(1)]})
        print(a)
if __name__ == '__main__':
    #func()
    func1()