#coding:utf8
import commands
import os
import chardet

def ssh_test():
    pdf_list=os.listdir('/Users/qmp/Desktop/announcement')
    for name in pdf_list:
        if name.endswith('.pdf'):
            print(name)
            # commands.getoutput('scp %s root@47.94.43.94:/alidata1/www/pdf1.qimingpian.com/announcement/%s'%(name,name))

#获取文件的编码方式
def file_chardetect():
    path='/Users/qmp/Desktop/'
    file_list=[x for x in os.listdir(path) if os.path.isfile(path+x)]
    for name in file_list:
        print(name)
        data=open(path+name,'rb').readline()
        file_type=chardet.detect(data)['encoding']
        print('encoding: ',file_type)

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

if __name__ == '__main__':
    # file_chardetect()
    # write_flag('2.343.123','a')
    s=read_flag()
    print(s)
    os.remove('./flag.txt')
    if s:
        s.remove('2.343.123')
        print(s)
        for i in s:
            write_flag(i,'a')


