#coding:utf8
import optparse
from socket import *
from threading import *
import nmap

#加锁操作
lock=Semaphore(value=1)

#测试连接端口是否开放
def connnect(tghost,tgport):
    try:
        CON=socket(AF_INET,SOCK_STREAM)
        CON.connect((tghost,tgport))
        CON.send('hihihihi...\n')
        result=CON.recv(100)
        lock.acquire()
        print('[+]%d/tcp open'%tgport)
        print('[+] receive info:'+str(result))
    except:
        lock.acquire()
        # pass
        print('[-]%d/tcp closed' % tgport)
    finally:
        lock.release()
        CON.close()

#扫描主机端口
def portscan(host,port):
    try:
        ip=gethostbyname(host)
    except:
        # print('[-]can not! %s:unknown host!'%host)
        return
    try:
        name=gethostbyaddr(ip)
        print('[+]scan name:%s'%name[0])
    except:
        print('[+]scan for %s!' % ip)
    setdefaulttimeout(1)
    for s in port:
        # print('scanning port! %s'%s)
        #使用多线程
        # s = Thread(target=connnect, args=(host, int(s)))
        s=Thread(target=nmap_scan,args=(host,s))
        s.start()

#nmap端口扫描
def nmap_scan(tghost,tgport):
    #/Users/qmp/envs/myproject/lib/python2.7/site-packages/nmap
    nscan=nmap.PortScanner()
    nscan.scan(tghost,tgport)
    state=nscan[tghost]['tcp'][int(tgport)]['state']
    print(tghost+ 'tcp/'+tgport+' state:'+str(state))
def main():
    parser=optparse.OptionParser("usage%porg "+"-H <target host> -p <target port>")
    parser.add_option('-H',dest='tghost',type='string',help='host help!')
    parser.add_option('-p',dest='tgport',type='string',help='port help!')
    (options,args)=parser.parse_args()
    tghost=options.tghost
    tgport=str(options.tgport).split(',')
    if (tghost==None) | (tgport[0]==None):
        print('input data null!!!')
        exit(0)
    portscan(tghost,tgport)
if __name__ == '__main__':
    main()
