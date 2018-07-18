#coding:utf8
from peewee import *
from playhouse.shortcuts import RetryOperationalError
import datetime
import ast
import time
import xlrd,xlwt



class RetryMySQLDatabase(RetryOperationalError, MySQLDatabase):
    pass

db = MySQLDatabase(
    host='47.94.42.90',
    database='shujujiance',
    user="readonly",
    passwd="pqRi2MXjFINsX1UP",
    charset='utf8'
)
URL_db = MySQLDatabase(
    host='47.94.38.128',
    database='shujujiance',
    user="shujujiance_pyt",
    passwd="f5W1vg##e1cf",
    charset='utf8'
)

def get_search_data(day,s_type):
    #搜索热度
    if s_type=='s':
        sql = 'select words,count(*) as num from search_magic_history where create_time regexp "%s" GROUP BY words order by num desc'%day
    #人物
    elif s_type=='p':
        sql="SELECT keywords,count(*) as num FROM mf_count_ip WHERE domain IN ('ios1.api.qimingpian.com','vip.api.qimingpian.com','pro.api.qimingpian.com','wx.api.qimingpian.com','az.qpi.qimingpian.com') AND ( keywords <> '' AND keywords <> '0|' AND keywords not like '%%%%|'  ) AND method = 'person' AND visit_time regexp '%s' GROUP BY keywords ORDER BY num desc"%day
    #项目
    elif s_type=='i':
        sql="SELECT `keywords`,count(*) as num FROM `mf_count_ip` WHERE `visit_time` regexp '%s' AND `method` IN ('c1','c3') AND `keywords` <> '' AND keywords not like '%%%%|' AND `domain` IN ('vip.api.qimingpian.com','ios1.api.qimingpian.com','pro.api.qimingpian.com','wx.api.qimingpian.com','az.api.qimingpian.com') GROUP BY keywords ORDER BY num desc"%day
    #机构
    elif s_type=='o':
        sql="SELECT `keywords`,count(*) as num FROM `mf_count_ip` WHERE `visit_time` regexp '%s' AND `method` = 'jigou3info' AND ( `keywords` <> '汉富资本' AND `keywords` <> '百场汇' AND `keywords` <> ''  ) AND `domain` IN ('vip.api.qimingpian.com','ios1.api.qimingpian.com','pro.api.qimingpian.com','wx.api.qimingpian.com','az.api.qimingpian.com') GROUP BY keywords ORDER BY num desc"%day
    else:
        sql=''
    print(sql)
    cur = db.execute_sql(sql)
    result = cur.fetchall()
    print(len(result))
    return result
    # print(result)



def read_excel(date):
    try:
        xlsfile = '/Users/qmp/Desktop/list_data_%s.xlsx'%date
        book = xlrd.open_workbook(xlsfile)  # 得到Excel文件的book对象，实例化对象
        sheet_name_list = book.sheet_names()  # 获得指定索引的sheet表名字
        for name in sheet_name_list:
            if name.encode('utf8').startswith(date):
                print(name)
                sheet1 = book.sheet_by_name(name)  # 通过sheet名字来获取，当然如果知道sheet名字就可以直接指定
                nrows = sheet1.nrows  # 获取行总数
                print("rows:"+str(nrows))
                # 循环打印每一行的内容
                s=[]
                for i in range(nrows):
                    d = {}
                    d[sheet1.row_values(i)[0]]=sheet1.row_values(i)[1]
                    s.append(d)
                with open('/Users/qmp/Desktop/hbase_data/list_data_%s.json'%''.join(date.split('-')),'w') as f:
                    f.write(str(s))
                print('save json ok!')
    except Exception as e:
        print(e)


def get_hz_ip_data(date):
    sql='select company from mf_product_company group by company'
    cusor=db.execute_sql(sql)
    com_list=map(lambda x:x[0],cusor.fetchall())
    print(len(com_list))
    sql0='select keywords,count(*) as num from mf_count_ip_hz where method = "wdproduct" and visit_time like "%s%%%%" GROUP BY keywords ORDER BY num desc'%date
    print(sql0)
    cusor1=db.execute_sql(sql0)
    hz_ip_list=cusor1.fetchall()
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('%s 数据统计'%date)
    i=0
    try:
        for s in hz_ip_list:
            if s[0] not in com_list and len(s[0])>3:
                    worksheet.write(i, 0, label=s[0])
                    worksheet.write(i, 1, label=s[1])
                    i += 1
        print('write ok!')
    except Exception as e:
        print(e)
    print('total number:',str(i))
    workbook.save('/Users/qmp/Desktop/list_data_%s.xlsx' % date)
    print('excel data save success!!')
    read_excel(str(date))


def select_max():
    sql='select max(id) from search_hot_key_history'
    res=URL_db.execute_sql(sql)
    info=res.fetchone()[0]
    return info if info else 0

def demo_test(date):
    print(date)
    sql = 'select words,count(*) as num from search_magic_history where create_time regexp "%s" and external_flag!=0 GROUP BY words order by num desc limit 10' % date
    cusor=URL_db.execute_sql(sql)
    result=cusor.fetchall()
    if result:
        for x in result:
            words=x[0]
            n=x[1]
            print(words,n)
            select_sql='select count(1) from search_hot_key_history where date_time=%s'%date
            cusor0=URL_db.execute_sql(select_sql)
            if cusor0.fetchone()[0]!=10:
                now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                add_sql='insert into search_hot_key_history(date_time,keyword,search_num,sort,create_time,update_time) value(%s,%s,%s,%s,%s,%s)'
                URL_db.execute_sql(add_sql,[date,words,n,select_max(),now,now])
                print('add ok!')
            else:
                print('is exist!!')



if __name__ == '__main__':
    path = '/Users/qmp/Desktop/hbase_data/'
    now_day = datetime.date.today()
    #昨天的记录
    # demo_test(str(now_day - datetime.timedelta(1)))

    for s_type in ['s','i','p','o']:
        time.sleep(0.3)
        # raw_data=get_search_data(str(now_day),s_type)
        for i in range(1,0,-1):
            before_day = str(now_day - datetime.timedelta(i))
            print(before_day)
            raw_data = get_search_data(str(before_day),s_type)
            dd = []
            for x in raw_data:
                ss = {}
                ss[x[0]] = str(x[1])
                dd.append(ss)
            # print(dd)
            if s_type=='i':
                base_name='item_data_'
            elif s_type=='o':
                base_name = 'org_data_'
            elif s_type=='p':
                base_name = 'person_data_'
            else:
                base_name = 'HBASE_data_'
            file_name=base_name+'%s.json'%''.join(str(before_day).split('-'))
            # if not os.path.exists(path+file_name):
            with open(path+file_name,'w') as f:
                f.write(str(dd))
            print('%s write ok!'%file_name)

    get_hz_ip_data(str(now_day - datetime.timedelta(1)))

    # with open(path + 'HBASE_data_201806.json', 'r') as f:
    #     data=f.read()
    # # print(data)
    # cc = []
    # for x in json.loads(data):
    #     ss = {}
    #     ss[x.keys()[0]] = str(x.values()[0])
    #     cc.append(ss)
    # with open(path + 'HBASE_data_20180612.json', 'w') as f:
    #     f.write(str(cc))
    # print('write ok!')
    # print(type(ast.literal_eval(data)))
    # print(type(json.loads(str(data))))
    # print(type(data))
    # s=eval(data)
    # print(s)
