#coding:utf8
import paramiko
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import time
import os

#监测多台服务器（包含爬虫部署主服务器）cpu利用率过高，发出警告邮件提醒。

server_name = {
    ###
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

        change_flag(ip)


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
        if avery_rate>=95.00:
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
            change_flag(ip)
            ssh.close()
        except:
            if ip not in read_flag():
                send_mail()
                write_flag(ip,'a')



def write_flag(ip,types):
    with open('./flag.txt', '%s'%types) as f:
        f.write(ip+'\n')

def read_flag():
    if os.path.exists('./flag.txt'):
        with open('./flag.txt', 'r') as f:
            data=f.readlines()
        data=map(lambda x:x.strip(),data)
    else:
        data=[]
    return data

def change_flag(ip):
    if ip in read_flag():
        data = read_flag()
        data.remove(ip)
        for i in data:
            write_flag(i, 'w')



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

    password=''
    sender = ''
    receiver = ""

    try:
        subject = '（%s）%s 服务器%s' % (server_name.get(ip), ip,mail_type)
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = 'listener<%s>' % sender
        msg['To'] = receiver
        smtp = smtplib.SMTP()
        # smtp.connect('smtp.163.com')
        smtp = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)


def main():
    master_server = {
        ####
    }
    cmd = 'top -bi -n 180 -d 1|grep -E "Cpu"'  # 间隔1s刷新一次，取样180次
    for ip, passwd in master_server.items():
        Cpu_handle(ip, 'root', passwd, cmd)

if __name__=='__main__':
    main()
