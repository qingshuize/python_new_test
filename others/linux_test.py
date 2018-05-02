#coding:utf8
import commands
import re,os
def send_mail_test():
    content='test mail,2322434'
    commands.getoutput('echo %s | mail -s "pyhton mail test from XXX" lf@qimingpian.com'%content)

def download_test():
    path='/Users/qmp/Desktop/'
    for type in ['guonei','guoji','mil','sports']:
        url='https://news.baidu.com/%s'%type
        file_name=type+'.html'
        status_file='status.txt'
        commands.getoutput('curl -I %s -D %s'%(url,path+status_file))
        with open(path+status_file,'r') as f:
            info=f.readline()
        os.remove(path+status_file)
        #print('delete file ok!')
        if re.findall(' \d+',info)[0].strip() == '200':
            commands.getoutput('curl %s -o %s --progress'%(url,path+file_name))
if __name__ == '__main__':
    #send_mail_test()
    download_test()
