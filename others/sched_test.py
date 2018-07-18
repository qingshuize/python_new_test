#coding:utf8

#定时任务设定
import os
import datetime
import time

#定时任务框架APScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
sched = BlockingScheduler()


#import sched
# def execute_command(cmd, inc):
#   '''''
#   终端上显示当前计算机的连接情况
#   '''
#   os.system(cmd)
#   schedule.enter(inc, 0, execute_command, (cmd, inc))
#
# def print_func(img,inc):
#     print('%s '%img)
#     schedule.enter(inc, 0, print_func, (img, inc))
#
#
# def main(inc=3):
#   # enter四个参数分别为：间隔时间、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
#   # 给该触发函数的参数（tuple形式）
#   schedule.enter(0, 0, print_func, ('xxxxx',inc))
#   schedule.enter(3, 100, print_func, ('yyyyy', inc))
#   schedule.run()



@sched.scheduled_job('interval', seconds=1)
def timed_job():
    print('xxxx.')


@sched.scheduled_job('cron', day_of_week='mon-fri', hour='18-19', minute='1-2', second='*/2')
def scheduled_job():
    print('This job is running... %s'%datetime.datetime.now())




if __name__ == '__main__':
    print('before the start funciton')
    sched.start()
    print("let us figure out the situation")

    # schedule = sched.scheduler(time.time, time.sleep)
    # main(0.5)
