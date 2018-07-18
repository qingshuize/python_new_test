#coding:utf8
import happybase
import datetime
import time,json,os
import ast

def main(date,num):
    try:
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_time = datetime.date.today().strftime('%Y%m%d')
        hour = time.localtime().tm_hour
        mintues = time.localtime().tm_min
        if (date > date_time or date < '20180416') and date != 'today':
            data = {
                'data': None,
                'update_time': now_time,
                'message': 'input data error',
                'status': -1,
            }
            print('null!!')
        else:
            if date == 'today':
                print('date:', date)
                date = date_time
        if date == date_time:
            select_hour = hour if mintues >= 35 else hour - 1
            select_hour = str(select_hour)
            select_hour = '0' + select_hour if len(select_hour) == 1 else select_hour   #小时数小于10前面补零

        else:
            select_hour = '23'  # 去每天最后一小时记录

        tablename = 'search_history_order_%s' % date
        ##
        conn = happybase.Connection('##')    
        table = conn.table(tablename)
        colum = 'order_value:'
        filter = "RowFilter(=,'regexstring:^%s')" % select_hour
        query = table.scan(filter=filter)
        result = list(query)
        row_key = result[0][0]
        value_data = result[0][1].get(colum)
        item = eval(value_data)
        print('total items:' + str(len(item)))
        # 截取前num条数据
        if num == 'all':
            n = None
        else:
            n = int(num)
        data = item[:n]
        print(len(data))
        # print(data)
        # try:
        #     with open('/Users/qmp/Desktop/hbase_data/HBASE_data_%s.json'%date,'wb') as f:
        #         f.write(json.dumps(data))
        #     print('ok!')
        # except Exception as e:
        #     print(e)

        # 关闭连接
        conn.close()
    except:
        data = None


class Hbase_getdata_test(object):
    # t_name = 'sssss'
    """
    host：主机名
    port：端口
    timeout：超时时间
    autoconnect：连接是否直接打开
    table_prefix：用于构造表名的前缀
    table_prefix_separator：用于table_prefix的分隔符
    compat：兼容模式
    transport：运输模式
    protocol：协议
    """
    def __init__(self):
        self.conn = happybase.Connection(host="##", port=9090)
        # ,timeout = None, autoconnect = True, table_prefix = None, table_prefix_separator = b'_', compat = '0.98', transport = 'buffered', protocol = 'binary')
    def create_t(self,table_name):
        families = {
            "order": dict(),
            "info": dict()
        }
        print(table_name)
        self.conn.create_table(table_name, families)
        print('create ok!')

        # t = conn.table(t_name)
        # # 按row前缀遍历查询数据，因该工程存入hbase的rowkey为id-timestamp，使用rowkey查询十分不方便，故使用row_prefix进行查询
        # for key, value in t.scan(row_prefix='row1'):
        #     print key, value

    def input_all_data(self):
        for file in os.listdir('/Users/qmp/Desktop/hbase_data/'):
            if file.endswith('json'):
                print(file)
                if file.startswith('item_data_'):
                    table_name = 'search_item_t'
                elif file.startswith('org_data_'):
                    table_name = 'search_org_t'
                elif file.startswith('person_data_'):
                    table_name = 'search_person_t'
                elif file.startswith('HBASE_data_'):
                    table_name = 'search_history_t'
                else:
                    table_name = 'search_company_t'
                with open('/Users/qmp/Desktop/hbase_data/%s'%file,'r') as f:
                    data=ast.literal_eval(f.read())
                    # data=json.loads(f.read())

                print(table_name)
                date=file[:-5].split('_')[-1]
                print(date)
                try:
                    if table_name not in self.conn.tables():
                        self.create_t(table_name)
                except:
                    pass
                finally:
                    if not self.conn.is_table_enabled(table_name):
                        self.conn.enable_table(table_name)
                    t = self.conn.table(table_name)
                    raw_data={
                        'order:info':'%s'%str(data)
                    }
                    t.put(row=date, data=raw_data)
                    # ##批量
                    # # bat = t.batch()
                    # # bat.put('row', data=raw_data)
                    # # bat.send()
                    print('input to hbase ok!')

    def update_data(self,date,s_type):

        if s_type=='i':
            base_name='item_data_'
            h_t='search_item_t'
        elif s_type=='o':
            base_name = 'org_data_'
            h_t = 'search_org_t'
        elif s_type=='p':
            base_name = 'person_data_'
            h_t = 'search_person_t'
        elif s_type=='s':
            base_name = 'HBASE_data_'
            h_t='search_history_t'
        else:
            base_name = 'list_data_'
            h_t = 'search_company_t'
        with open('/Users/qmp/Desktop/hbase_data/%s%s.json' % (base_name,date), 'r') as f:
            data = ast.literal_eval(f.read())

        if h_t not in self.conn.tables():
            self.create_t(h_t)
        t = self.conn.table(h_t)
        raw_data = {
            'order:info': '%s' % str(data)
        }
        t.put(row=date, data=raw_data)
        print('update %s %s hbase data ok!'%(h_t,date))

    def get_data(self,name):

        table = happybase.Table(name, self.conn)
        content = table.cells('row', 'order:info')
        list0=eval(content[0])
        print(type(list0))
        print(len(list0))
        print(list0[0])
        # print(eval('%s'%content[0]))

    def drop_all_t(self):
        t_list=self.conn.tables()
        print(t_list)
        for x in t_list:
            #name：表名
            #disable：是否先禁用表
            self.conn.delete_table(x,disable=True)
            print('delete %s ok!'%x)





    # conn = happybase.Connection('##') 
    # conn.open()
    # t_list=conn.tables()
    # print(t_list)
    # table = conn.table(t_name, user_prefix=True)
    # colum = 'row1:'
    # query = table.scan()
    # result = list(query)
    # print(result)
    # row_key = result[0][0]
    # value_data = result[0][1].get(colum)
    # item = eval(value_data)
    # print(item)
    def close_h(self):
        self.conn.close()

if __name__ == '__main__':
    # for i in range(80):
    #     date=str(datetime.datetime.now()-datetime.timedelta(i)).split(' ')[0].replace('-','')
    #     print(date)
    # main(date,'all')
    h_s=Hbase_getdata_test()
    # h_s.create_t('search_1000')
    # h_s.get_data('search_history_order_20180625')
    # h_s.input_all_data()
    # h_s.drop_all_t()
    date=(datetime.date.today()-datetime.timedelta(1)).strftime('%Y%m%d')
    for s_type in ['s','i','p','o','c']:
        h_s.update_data(date,s_type)
        # h_s.input_all_data()
    h_s.close_h()
