#coding:utf8
import pexpect
import paramiko
import threading
import re,time,datetime
import os
import requests
from peewee import *
URL_db = MySQLDatabase(
    host='47.94.38.128',
    database='shujujiance',
    user="shujujiance_pyt",
    passwd="f5W1vg##e1cf",
    charset='utf8'
)

def ganggu_zhaogu_link_real():
    sql='select id,qmp_url,file_size from mf_hk_zhaogu where qmp_url is not null and qmp_url!="" and link_is_real=0 limit 3'
    cur=URL_db.execute_sql(sql)
    res=cur.fetchall()
    for x in res:
        id=x[0]
        url=x[1]
        size=x[2]
        file_name=url.split('/')[-1]
        get_size=os.path.getsize('ganggu/'+file_name)
        if get_size!=size:
            print('id:'+str(id))

def ssh_login(ip,username,passwd,cmd):
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
                print(info)
                ganggu_zhaogu_link_real()

        print(30 * '*' + '%s close' % ip + 30 * '*'+'\n')
        ssh.close()
    except Exception as e:
        print(e)
        print('%s\tError\n'%(ip))

if __name__ =='__main__':
    server_list=['47.94.43.94','1993fileWL0301']
    #ps -aux|grep phantomjs
    cmd = ['source /alidata/qmp_code/qmp_venv/bin/activate','cd /alidata1/www/pdf1.qimingpian.com']
    print("start... ... ... ...")
    ssh_login(server_list[0],'root',server_list[1],cmd)