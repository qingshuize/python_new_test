#coding:utf8
import pexpect
import paramiko
import threading
import re,time,datetime

def ssh_login(ip,username,passwd,cmd,unit='秒'):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=10)
        for m in cmd:
            print(30 * '-' + '%s connected' % ip + 30 * '-'+'\n')
            stdin, stdout, stderr = ssh.exec_command(m)
            stdin.write("Y")
            out = stdout.readlines()
            for info in out:
                # if len(out) > 1:
                # for info in out[:-1] if '-aux' in m else out[1:]:
                # if 'crawl' in info:
                    try:
                        raw_start_time=re.findall(' \d+:[\d+:]+',info)[0]
                        start_time=datetime.datetime.strptime(datetime.date.today().strftime('%Y-%m-%d')+' '+raw_start_time,'%Y-%m-%d %H:%M')
                        print('start time:' + str(start_time))
                        now_time=datetime.datetime.now()
                        s=3600.0 if unit=='小时' else 60.0 if unit=='分钟' else 1.0
                        run_time=(now_time-start_time).seconds/s
                        if run_time>=1:
                            print('servers ip:'+ip)
                            print('info:' + info)
                            pid = re.findall('root(.*)',info)[0].strip().split(' ')[0]
                            print('pid:' + pid)
                            print('\nselect long time: %0.2f%s'%(run_time,unit))
                            if 'phantomjs' in info or 'ganggu_industry' in info:
                                ssh.exec_command('kill -9 %s'%pid)
                                print('kill ok!')

                    except Exception as e:
                        print(e)
        print(30 * '*' + '%s close' % ip + 30 * '*'+'\n')
        ssh.close()
    except Exception as e:
        print(e)
        print('%s\tError\n'%(ip))



if __name__ =='__main__':
    server_dict = {
        '123.206.55.84': 'kF4hMs4mk6sGW',
        '123.206.6.125': 'YdWa9fdPD4Myp2F',
        '123.206.49.157': 'YdWa9fdPD4Myp2F',
        '123.206.84.240': 'YdWa9fdPD4Myp2F',
        '123.206.15.238': 'YdWa9fdPD4Myp2F',
        '123.207.162.192': 'YdWa9fdPD4Myp2F',
        '139.199.97.233': 'sh9vSGMinwr',
        '123.206.46.158': '55fIecQIETuhZR',
        '123.206.73.147': 'tXDmVLUMq9CDY',
        '123.206.60.97': 'kF4hMs4mk6sGW',
        '47.94.43.94': '1993fileWL0301',
        '47.95.36.57': '1993newsWL0301'
    }
    #ps -aux|grep phantomjs
    cmd = ['ps -aux|grep -e "crawl" -e "phantomjs"']
           #,'ps -ef|grep crawl']  # 你要执行的命令列表
    # for i in range(1,4):
    #     print(40*'~'+'THE %s ROUNDS'%i+40*'~')
    #'分钟'，'小时', 默认单位：'天'
    for addr,passwd in server_dict.items():
        username = "root"
        threads = []
        print("start... ... ... ...")
        a = threading.Thread(target=ssh_login, args=(addr, username, passwd, cmd,'小时'))
        a.start()
        # time.sleep(5)
        a.join()
        # time.sleep(10)