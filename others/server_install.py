#coding:utf8
##在多台服务器虚拟环境下上安装所需的包
import paramiko
import time,sys


def Server_pip_install(ip,username,passwd,cmd,package):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip,22,username,passwd)
        print('\n' + 50 * '-' + '%s connected' % ip + 60 * '-' + '\n')
        env_path = '/xx' if ip in [] else '/xxx'
        stdin, stdout, stderr = ssh.exec_command(cmd%((env_path,package) if 'yum' not in cmd else package))
        # stdin, stdout, stderr = ssh.exec_command(cmd % package)
        stdin.write("Y")
        print('successfully connect!!')
        out = stdout.readlines()
        for info in out:
            try:
                print(info)
            except Exception as e:
                print(e)

        print('\n'+60 * '#' + '%s close' % ip + 60 * '#'+'\n')
        ssh.close()
    except Exception as e:
        print(e)
        print('%s\t connect Error!!!\n'%(ip))



if __name__ =='__main__':
    server_dict = {
       ######
    }
    yum_cmd='sudo add-apt-repository ppa:coolwanglu/pdf2htmlex;yum -y install %s'
    cmd = 'source %s/envs/bin/activate;pip install %s;pip list'
    #'xlrd' #'xlwt'
    try:
        package=sys.argv[-1]
        print(package)
        # package='pdf2htmlEX'
        for addr,passwd in server_dict.items():
            try:
                username = "root"
                Server_pip_install(addr, username, passwd, yum_cmd, package)
                time.sleep(1)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
