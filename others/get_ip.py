#coding:utf8
import socket
import platform
import struct
import fcntl
import uuid
import os,sys

def getipaddrs(hostname):
    result = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)
    return [x[4][0] for x in result]


#获取mac地址
def get_mac():
    mac = None
    if sys.platform == "win32":
        for line in os.popen("ipconfig /all"):
            if line.lstrip().startswith("Physical Address"):
                mac = line.split(":")[1].strip().replace("-", ":")
                break
    else:
        node = uuid.getnode()
        mac = uuid.UUID(int = node).hex[-12:]
    return mac

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        pass
    finally:
        s.close()

    return ip

if __name__ == "__main__":
    # mac_ip_list=get_mac().split(':')
    # print(get_mac())
    hostname = socket.gethostname()
    try:
        print('ip:'+get_host_ip())
        # print("IP addresses:"+" ".join(getipaddrs(hostname)))
    except socket.gaierror as e:
        print("Couldn't not get IP addresses:")



    # ip_address = "0.0.0.0"
    # sysstr = platform.system()
    # print(sysstr)
    # if sysstr == "Windows":
    #     ip_address = socket.gethostbyname(socket.gethostname())
    #     print "Windows @ " + ip_address
    # elif sysstr == "Linux":
    #     ip_address = getip()
    #     print "Linux @ " + ip_address
    # elif sysstr == "Darwin":
    #     ip_address = socket.gethostbyname(socket.gethostname())
    #     print "Mac @ " + ip_address
    # else:
    #     print "Other System @ some ip"

# if __name__=='__main__':
#     addrs = socket.getaddrinfo(socket.gethostname(), None)
#
#     for item in addrs:
#         print(item)
#
#     # 仅获取当前IPV4地址
#     print('当前主机IPV4地址为:' + [item[4][0] for item in addrs if ':' not in item[4][0]][0])
#
#     # 同上仅获取当前IPV4地址
#     for item in addrs:
#         if ':' not in item[4][0]:
#             print('当前主机IPV4地址为:' + item[4][0])
#             break