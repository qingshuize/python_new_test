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


if __name__ == '__main__':
    file_chardetect()