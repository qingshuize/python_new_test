#coding:utf8
import paramiko
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime

#监测爬虫部署主服务器cpu利用率过高，发出警告邮件提醒。

def Cpu_handle(ip, username, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username, passwd)
        print('\n' + 50 * '-' + '%s connected' % ip + 60 * '-' + '\n')
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.write("Y")
        print('successfully connect!!')
        out = stdout.readlines()
        cpu_use_rate_list=[]
        print('wait! ... ...')
        for x in out:
            print(x)
            cpu_use_rate=x.split(':')[-1].strip().split(',')[0][:-2].strip()
            print('cpu use rate:'+cpu_use_rate)
            if cpu_use_rate!='0.0':
                cpu_use_rate_list.append(float(cpu_use_rate))
        avery_rate=float('%.2f'%(sum(cpu_use_rate_list)/len(cpu_use_rate_list)))
        print('CPU平均使用率:'+str(avery_rate)+'%')
        if avery_rate>=90.00:
            now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            text = '''
            Warning!!! The master server cpu usage is too high more than %s%%...
            ...
            create_time:%s
            '''%(avery_rate,now)
            msg = MIMEText(text, 'plain', 'utf-8')

            username='15313862350'
            password='199377Lf'
            sender='15313862350@163.com'
            receiver = "lf051@qimingpian.com"

            try:
                subject = '爬虫主服务器CPU报警'
                msg = MIMEText(text, 'plain', 'utf-8')
                msg['Subject'] = Header(subject, 'utf-8')
                msg['From'] = 'listener<%s>'%sender
                msg['To'] = receiver
                smtp = smtplib.SMTP()
                smtp.connect('smtp.163.com')
                smtp.login(username, password)
                smtp.sendmail(sender, receiver, msg.as_string())
                smtp.quit()
                print("邮件发送成功")
            except smtplib.SMTPException as e:
                print(e)

    except Exception as e:
        print(e)

if __name__=='__main__':
    master_server={
        '123.206.29.196':'tXDmVLUMq9CDY'
    }
    cmd='top -bi -n 60 -d 0.5|grep -E "Cpu"'   #间隔0.5s刷新一次，取样50次
    ip=master_server.keys()[0]
    passwd=master_server.values()[0]
    Cpu_handle(ip,'root',passwd,cmd)