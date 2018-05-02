#coding:utf8
import paramiko
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import time

#监测多台服务器（包含爬虫部署主服务器）cpu利用率过高，发出警告邮件提醒。

server_name = {
    '123.206.29.196': '爬虫主服务器',
    '39.107.205.65': '大数据主服务器',
    '39.107.204.13': '大数据从服务器',
    '139.199.97.167': 'supervisor服务器监控',
    '123.206.73.147': '爬虫服务器slave1'
}

def Cpu_handle(ip, username, passwd, cmd):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username, passwd)
        print('\n' + 50 * '-' + '%s connected' % ip + 60 * '-' + '\n')
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.write("Y")
        print('%s 已成功连接!!'%server_name.get(ip))
        out = stdout.readlines()
        cpu_use_rate_list=[]
        print('wait! ... ...')
        for x in out:
            # print(x)
            cpu_use_rate=x.split(':')[-1].strip().split(',')[0][:-2].strip()
            print('cpu use rate:'+cpu_use_rate+'%')
            if cpu_use_rate!='0.0':
                cpu_use_rate_list.append(float(cpu_use_rate))
        avery_rate=float('%.2f'%(sum(cpu_use_rate_list)/len(cpu_use_rate_list)))
        print('%s CPU平均使用率:'%server_name.get(ip) +str(avery_rate)+'%')
        if avery_rate>=98.00:
            send_mail(avery_rate=avery_rate,mail_type='CPU使用率报警')

        ssh.close()

    except Exception as e:
        print(e)
        print(20*'//'+'server:%s connect error! try again!!'%ip+20*'//')
        try:
            time.sleep(1)
            ssh.connect(ip, 22, username, passwd)
            time.sleep(0.5)
            print('ok!  %s 已成功连接!!' % server_name.get(ip))
            ssh.close()
        except:
            send_mail()


def send_mail(avery_rate=None,mail_type='SSH连接异常'):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if mail_type=='cpu attention':
        text = '''
                    Attenion!!! The server cpu usage is too high more than %s%%...
                    ...
                    create_time:%s
                    ''' % (avery_rate, now)
    else:
        text = '''
                    Warning!!! The server can not connect! ...
                    ...
                    create_time:%s
                    ''' % now

    username = '15313862350'
    password = '199377Lf'
    sender = '15313862350@163.com'
    receiver = "lf051@qimingpian.com"

    try:
        subject = '（%s）%s 服务器%s' % (server_name.get(ip), ip,mail_type)
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = 'listener<%s>' % sender
        msg['To'] = receiver
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com')
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)


if __name__=='__main__':
    master_server={
        '123.206.29.196':'tXDmVLUMq9CDY',
        '39.107.205.65': '19930301qiMBpG',  # 大数据主服务器
        '39.107.204.13': '19930301qiMBpG',   # 大数据从服务器
        '139.199.97.167':'sh9vSGMinwr',        #supervisor服务器监控
        '123.206.73.147': 'tXDmVLUMq9CDY'
    }
    cmd='top -bi -n 180 -d 1|grep -E "Cpu"'   #间隔1s刷新一次，取样180次
    for ip,passwd in master_server.items():
        Cpu_handle(ip,'root',passwd,cmd)