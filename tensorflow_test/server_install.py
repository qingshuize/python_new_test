#coding:utf8
##在多台服务器虚拟环境下上安装所需的包
import paramiko
import time

def Server_pip_install(ip,username,passwd,cmd,package):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip,22,username,passwd)
        print('\n' + 50 * '-' + '%s connected' % ip + 60 * '-' + '\n')
        env_path = '/alidata/qmp_code' if ip in ['47.94.43.94','47.95.36.57'] else '/qmp_code'
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
        # '123.206.73.147': 'tXDmVLUMq9CDY',
        # '123.206.84.240': 'YdWa9fdPD4Myp2F',
        # '123.206.15.238': 'YdWa9fdPD4Myp2F',
        '47.94.43.94': '1993fileWL0301',
        # '123.206.6.125': 'YdWa9fdPD4Myp2F',
        # '123.207.162.192': 'YdWa9fdPD4Myp2F',
        # '123.206.46.158': '55fIecQIETuhZR',
        # '123.206.60.97': 'kF4hMs4mk6sGW',
        # '123.206.77.105': 'kF4hMs4mk6sGW',
        # '123.206.49.157': 'YdWa9fdPD4Myp2F',
        '47.95.36.57': '1993newsWL0301',
        # '123.206.55.84': 'kF4hMs4mk6sGW',
        # '139.199.97.233': 'sh9vSGMinwr'
    }
    yum_cmd='sudo add-apt-repository ppa:coolwanglu/pdf2htmlex;yum -y install %s'
    cmd = 'source %s/qmp_venv/bin/activate;pip install %s;pip list'
    #'xlrd' #'xlwt'
    package='pdf2htmlEX'
    for addr,passwd in server_dict.items():
        try:
            username = "root"
            Server_pip_install(addr, username, passwd, yum_cmd, package)
            time.sleep(1)
        except Exception as e:
            print(e)
