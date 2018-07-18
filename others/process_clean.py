#coding:utf8

import paramiko
import re
import datetime
from threading import *
from multiprocessing import Process

def ssh_login(ip,username,passwd,cmd,limit_hour=''):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd)
        print('\n' + 50 * '-' + '%s connected' % ip + 60 * '-' + '\n')
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            stdin.write("Y")
            print('successfully connect!!')
            out = stdout.readlines()
            for info in out:
                try:
                    if not re.findall('(save_totalnew_html_spider|save_onenew_html_spider)', info):
                        pid = re.findall('root(.*)', info)[0].strip().split(' ')[0]

                        try:
                            #不是当天，获取日期
                            now_year=datetime.date.today().year
                            raw_start_time=re.findall(r'[A-Za-z]+\d{2}',info)[0]
                            raw_start_time=datetime.datetime.strptime(str(now_year)+raw_start_time,"%Y%b%d")
                            print('超时间:开始于%s' % str(raw_start_time))
                            print('info:' + info)
                            run_day = (datetime.datetime.now()-raw_start_time).days
                            print('运行天数：' + str(run_day))
                            if run_day > 1 or re.findall('(phantomjs|totalnews_img_save)', info):
                                ssh.exec_command('kill -9 %s' % pid)
                                print('kill ok!')

                        except:
                            raw_start_time = re.findall(r'\d+:\d+', info)[0]

                            time_run = re.findall('\d+:\d+', info)[1]
                            hour = time_run.split(':')[0].encode('utf8')
                            minute = time_run.split(':')[1].encode('utf8')

                            start_time=datetime.datetime.strptime(datetime.date.today().strftime('%Y-%m-%d')+' '+raw_start_time,'%Y-%m-%d %H:%M')
                            print('start time:' + str(start_time))
                            now_time = datetime.datetime.now()
                            # s = 3600.0 if unit == '小时' else 60.0 if unit == '分钟' else 1.0
                            run_time_hour = (now_time - start_time).seconds / 3600
                            run_time_minute=((now_time - start_time).seconds-run_time_hour*3600)/60

                            if (run_time_minute>=40 and run_time_hour==0) or run_time_hour>0:
                                print('info:' + info)
                                print('servers ip:' + ip)
                                print('time_run:%s小时%s分钟' %(run_time_hour,run_time_minute))
                                try:
                                    if re.findall('(phantomjs|shenbao|jiguan|ganggu_industry|ipo_csrc_pdf)', info):
                                        ssh.exec_command('kill -9 %s' % pid)
                                        print('kill ok!')
                                except Exception as e:
                                    print(e)
                                    print('略过...')

                except Exception as e:
                    print(e)
            ssh.close()
            print('\n' + 60 * '#' + '%s close' % ip + 60 * '#' + '\n')


    except Exception as e:
        print(e)
        print('%s\t connect Error!!!\n'%(ip))




if __name__ =='__main__':
    server_dict = {
        ########
    }

    ##执行的指令
    # cmd=['ps -ef|grep -e "catch_thrift.py" -e "hbase-daemon.sh"']
    cmd = ['ps -aux|grep -e "crawl" -e "phantomjs" -e "Xvfb -br"']
    # for i in range(1,4):
    #     print(40*'~'+'THE %s ROUNDS'%i+40*'~')
    #'分钟'，'小时', 默认单位：'天'
    # for _ in range(4):
    # lock = Semaphore(1)
    username = "root"
    for addr,passwd in server_dict.items():
        ssh_login(addr, username, passwd, cmd)
        # s=Process(target=ssh_login,args=(addr, username, passwd, cmd))
        # s.start()

