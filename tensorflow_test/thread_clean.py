#coding:utf8
import paramiko
import threading
import re
import datetime

def ssh_login(ip,username,passwd,cmd,limit_hour=''):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip,22,username,passwd)
        print('\n' + 50 * '-' + '%s connected' % ip + 60 * '-' + '\n')
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            stdin.write("Y")
            print('successfully connect!!')
            out = stdout.readlines()
            for info in out:
                try:
                    try:
                        raw_start_time=re.findall(r'[A-Za-z]+\d{2}',info)[0]
                        raw_start_time=datetime.datetime.strptime(raw_start_time+str(datetime.date.today())[:4]
,'%b%d%Y')
                    except Exception:
                        raw_start_time = re.findall(r'\d+:\d+', info)[0]

                    time_run = re.findall('\d+:\d+', info)[1]
                    hour = time_run.split(':')[0].encode('utf8')
                    minute = time_run.split(':')[1].encode('utf8')
                    pid = re.findall('root(.*)', info)[0].strip().split(' ')[0]


                    if len(str(raw_start_time))>5:
                    # if hour>='12':
                        print('超时间:开始于%s'%str(raw_start_time))
                        print('info:' + info)
                        print(raw_start_time)
                        now_time = datetime.datetime.now()
                        run_day=(now_time - raw_start_time).days
                        print('运行天数：'+str(run_day))
                        if run_day>=2 or re.findall('(phantomjs|shenbao|jiguan)', info):
                            ssh.exec_command('kill -9 %s' % pid)
                            print('kill ok!')
                    else:
                        start_time=datetime.datetime.strptime(datetime.date.today().strftime('%Y-%m-%d')+' '+raw_start_time,'%Y-%m-%d %H:%M')
                        print('start time:' + str(start_time))
                        now_time = datetime.datetime.now()
                        # s = 3600.0 if unit == '小时' else 60.0 if unit == '分钟' else 1.0
                        run_time_hour = (now_time - start_time).seconds / 3600
                        run_time_minute=((now_time - start_time).seconds-run_time_hour*3600)/60
                        if not re.findall('Xvfb -br', info):
                            if (run_time_minute>=40 and run_time_hour==0) or run_time_hour>0:
                                print('info:' + info)
                                print('servers ip:' + ip)
                                print('time_run:%s小时%s分钟' %(run_time_hour,run_time_minute))
                                try:
                                    if re.findall('(phantomjs|shenbao|jiguan)', info):
                                        ssh.exec_command('kill -9 %s' % pid)
                                        print('kill ok!')
                                except Exception as e:
                                    print(e)
                                    print('略过...')

                except Exception as e:
                    print(e)

        print('\n'+60 * '#' + '%s close' % ip + 60 * '#'+'\n')
        ssh.close()
    except Exception as e:
        print(e)
        print('%s\t connect Error!!!\n'%(ip))



if __name__ =='__main__':
    server_dict = {
        '123.206.73.147': 'tXDmVLUMq9CDY',
        '123.206.84.240': 'YdWa9fdPD4Myp2F',
        '123.206.15.238': 'YdWa9fdPD4Myp2F',
        '47.94.43.94': '1993fileWL0301',
        '123.206.6.125': 'YdWa9fdPD4Myp2F',
        '123.207.162.192': 'YdWa9fdPD4Myp2F',
        '123.206.46.158': '55fIecQIETuhZR',
        '123.206.60.97': 'kF4hMs4mk6sGW',
        '123.206.77.105': 'kF4hMs4mk6sGW',
        '123.206.49.157': 'YdWa9fdPD4Myp2F',
        '47.95.36.57': '1993newsWL0301',
        '123.206.55.84': 'kF4hMs4mk6sGW',
        '139.199.97.233': 'sh9vSGMinwr'
        # '39.107.205.65':'19930301qiMBpG'  #大数据服务器
    }
    #ps -aux|grep phantomjs

    # cmd=['ps -ef|grep -e "catch_thrift.py" -e "hbase-daemon.sh"']
    cmd = ['ps -aux|grep -e "crawl" -e "phantomjs" -e "Xvfb -br"']
           #,'ps -ef|grep crawl']  # 你要执行的命令列表
    # for i in range(1,4):
    #     print(40*'~'+'THE %s ROUNDS'%i+40*'~')
    #'分钟'，'小时', 默认单位：'天'
    # for _ in range(4):
    for addr,passwd in server_dict.items():
        username = "root"
        ssh_login(addr, username, passwd, cmd)
