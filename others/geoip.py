#coding:utf8

#依据IP地址查询所在地区物理位置信息
import pygeoip
import requests
def Geoip_handle(ip_addr):
    g=pygeoip.GeoIP('/Users/qmp/Desktop/GeoIP/GeoLiteCity.dat')
    recv=g.record_by_name(ip_addr)
    print(recv.keys())
    city=recv.get('city')
    continent=recv.get('continent')
    country=recv.get('country_name')
    long=recv.get('longitude')
    lat=recv.get('latitude')
    region_code=recv.get('region_code')
    print('city:'+city)
    print('country:'+country)
    print('continent:'+continent)
    print('region_code:'+region_code)
    print('logitude:%s latitude:%s'%(long,lat))

if __name__ == '__main__':
    #192.168.1.56
    #39.155.188.22
    ##localIP:
    # my_ip_info=commands.getoutput('ifconfig|grep -E "inet(.*)broadcast"')
    # print(my_ip_info)
    # my_ip=''.join(re.findall('[\d+\W]{3}\d+',my_ip_info)[:3]).strip()
    # print(my_ip)

    ##globalIP
    get_my_global_ip_info=requests.get('http://icanhazip.com/')
    get_my_global_ip=get_my_global_ip_info.text.encode('utf8').rstrip('\n')
    print(get_my_global_ip)
    Geoip_handle(get_my_global_ip)