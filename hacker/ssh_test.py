#coding:utf8
import pexpect

PROMPT=['#',', ','>>>','>',', '+'\$ ']

def send_cmd(child,cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)

def connect(user,host,passwd):
    ssh_key='something wrong!'
    conn='ssh '+user+'@'+host
    child=pexpect.spawn(conn)
    ret=child.expect([pexpect.TIMEOUT,ssh_key,'[P|p]assword:'])
    if ret==0:
        print('error connecting!')
        return
    if ret==1:
        child.sendline('yes')
    ret=child.expect([pexpect.TIMEOUT,'[P|p]assword:'])
    if ret==0:
        print('error connecting!')
        return
    child.sendline(passwd)
    child.expect(PROMPT)
    return child


if __name__ == '__main__':
    host='localhost'
    user='root'
    passwd='123'
    child=connect(user,host,passwd)
    send_cmd(child,'cat /etc/shadow |grep root')