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

if __name__ == '__main__':
    func()