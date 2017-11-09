#coding:utf8
import tensorflow as ten
import numpy as num
import math
import matplotlib.pyplot as plt
import csv
import datetime
import json,re,os
import pygal
from pygal.style import RotateStyle
from pygal.style import LightStyle,LightColorizedStyle #使用明亮主题颜色
from pygal_maps_world.i18n import COUNTRIES
from pygal_maps_world.maps import World
from datapackage import Package


def trace_handle(fun):
    def wrapper(*args,**kwargs):
        try:
            return fun(*args,**kwargs)
        except Exception as e:
            print(e)
            print('-----Error-----')
    return wrapper


def func():
    a=ten.Variable(0,name='s')
    b=ten.constant(2)
    value=ten.add(a,b)
    update=ten.assign(a,value)

    init_op=ten.initialize_all_variables()
    with ten.Session() as se:
        se.run(init_op)
        for _ in range(5):
            result=se.run(update)
            print(result)
def func1():
    x=ten.placeholder(ten.float64)
    y=ten.placeholder(ten.float64)
    output=ten.add(x,y)
    #output=plt.plot(x,y)
    with ten.Session() as se:
        a=se.run([output], feed_dict={x:[num.random.random([4])],y:[num.random.random([4])]})
        print(a)


def func2():
    x1=num.random.random([100])
    y1=num.random.random([100])
    x2=num.random.random_sample([200])
    y2=num.random.random_sample([200])
    plt.plot(x1,y1,linewidth=1,c='red')
    plt.plot(x2,y2,c='blue')
    plt.title('test plot')
    plt.xlabel('x random series',fontsize=12)
    plt.ylabel('y random series',fontsize=12)
    plt.tick_params(axis='both',labelsize=12)
    plt.show()

def f_function():
    pi=math.pi
    x=num.float64(range(0,10))
    y=num.sin(2*pi*x)
    plt.plot(x,y,c='black')
    plt.show()


def csv_data():
    with open('/Users/qmp/Downloads/weather.csv') as f:
        reader=csv.reader(f)
        #header_row=next(reader)
        #for index,column in enumerate(header_row):
        #    print(index,column)
        date_list,data_list,data_list1=[],[],[]
        for x in reader:
            date_list.append(datetime.datetime.strptime(x[0],'%Y-%m-%d'))
            print(x[1])
            data_list.append(x[1])
            data_list1.append(x[-1])
    fig=plt.figure(dpi=128,figsize=(10,6))
    plt.plot(date_list,data_list,c='blue',alpha=0.7,linewidth=1)
    plt.plot(date_list,data_list1,c='red',alpha=0.6,linewidth=0.5)
    plt.fill_between(date_list,data_list,data_list1,facecolor='yellow',alpha=0.2)
    plt.title('weather data')
    plt.xlabel('Time',fontsize=14)
    plt.ylabel('Temperature (C)',fontsize=14)
    fig.autofmt_xdate()
    plt.tick_params(axis='both',which='major',labelsize=10)
    plt.show()

def counrty_list_show(coun):
    for code,name in COUNTRIES.items():
        if name==coun:
            return code

def world_map_test():
    map_style=RotateStyle('#44ff77')
    map=World(style=map_style)
    map.title='world map scope'
    country_list=[]
    chinese_name={
                'United States': u'大美利坚',
                'United Kingdom': u'大英帝国',
                'France': u'法兰西',
                'Italy':  u'意大利',
                'Japan':  u'东瀛',
                'Germany': u'德意志',
                'Canada':  u'加拿大'
                }


    detail_dict={}
    print(type(chinese_name))
    for code,name in COUNTRIES.items():
        if name in ('United States','United Kingdom','France','Italy','Japan','Germany','Canada'):
            country_list.append(code)
            print(code)
        if name == 'Russian Federation':
            unique=code
    print(country_list)
    map.add(u'G7国家',country_list)
    #map.add(u'G8国家',country_list+[unique])
    map.render_to_file('/Users/qmp/Desktop/map1.svg')

@trace_handle
def json_data_handle():
    gdp_style=RotateStyle('#5555ff')
    map=World(style=gdp_style)
    package = Package('/Users/qmp/Downloads/gdp.zip')
    resources = package.descriptor['resources']
    resourceList = [resources[x]['name'] for x in range(0, len(resources))]
    #print(resourceList)
    data = package.resources[0].read()
    show_dict={}
    for x in data:
        if x[2]==2016:
            code=counrty_list_show(x[0])
            #print(code,x)
            gdp=long(x[-1])
            print(gdp)
            show_dict[code]=gdp
    print(show_dict)
    map.title=u'2016世界所有经济体GDP'
    map.add(u'经济体',show_dict)
    map.render_to_file('/Users/qmp/Desktop/map_gdp.svg')

@trace_handle
def csv_data_handle():
    with open('/Users/qmp/Downloads/API_TX.VAL.TECH.MF.ZS_DS2_en_csv_v2/API_TX.VAL.TECH.MF.ZS_DS2_en_csv_v2.csv') as f:
        reader=csv.reader(f)
        #print(next(reader))
        map_style=RotateStyle('#4455ee',base_style=LightStyle)
        map=World()
        info_dict={}
        for x in reader:
            if len(x)==62:
                print(x[0],x[1],x[-2])
                code=counrty_list_show(x[0])
                info_dict[code]=float((x[-2])) if x[-2] !='' else None
        map.title='High-technology exports (% of manufactured exports)'
        map.add('',info_dict)
        map.render_to_file('/Users/qmp/Desktop/High_Tech_map.svg')


@trace_handle
def json_use():
    package=Package('https://api.github.com/search/repositories?q=language:python&sort=stars')
    show_data={}
    top=0
    name,stars=[],[]
    for x in package.descriptor['items']:
        name.append(x['name'])
        stars.append(x['stargazers_count'])
        #print('ssh_url:'+'http://'+x['ssh_url'])
        #print('git_url:'+x['git_url'])
        if x['watchers_count']>top:
            show_data['top']=x['watchers_count']
            show_data['updated_time']=x['updated_at']
            show_data['git_url'] = x['git_url']
            show_data['stargazers_count']=x['stargazers_count']
            top=x['watchers_count']
    print('update_time:'+show_data['updated_time'])
    print('watchers_count:',show_data['top'])
    print('stargazers_count:', show_data['stargazers_count'])
    print('git_url:'+ show_data['git_url'])

    data_style = RotateStyle('#333377', base_style=LightColorizedStyle)
    data_img = pygal.Bar(x_label_rotation=70,style=data_style,show_legend=False)
    data_img.title='Stars Python Project in Github Bar'
    data_img.x_labels=name
    data_img.render_to_png('/Users/qmp/Desktop/High_Tech_map.png')
    #data_img.add('stars number',stars)
    #data_img.render_to_file('/Users/qmp/Desktop/python_bar.svg')

if __name__ == '__main__':
    #func()
    #func1()
    #func2()
    #f_function()
    #csv_data()
    #counrty_list_show()
    #world_map_test()
    #json_data_handle()
    #csv_data_handle()
    json_use()
