#coding:utf8
import redis
import elasticsearch
import datetime
import time
import random
import re
from modles import SJJC_db,Person_card_tagsModel
from elasticsearch import ElasticsearchException
from elasticsearch.helpers import bulk
from elasticsearch import Transport
from elasticsearch.connection import RequestsHttpConnection


class Data_flow(object):
    def get_all_data(self):
        sql="select unionid as _id, GROUP_CONCAT(distinct(tag)) as tags, display_flag, update_time from person_card_tags group by unionid"#update_time >= now()
        cusor = SJJC_db.execute_sql(sql)
        ress = cusor.fetchall()
        return ress

    def get_tag(self):
        sql = 'select distinct(tag) from mf_product_tags order by id limit 3000'
        cusor = SJJC_db.execute_sql(sql)
        ress=cusor.fetchall()
        return  ress

    def get_name(self):
        sql='select name from mf_person_info where name!="" and name is not null order by id limit 200,100'
        cusor = SJJC_db.execute_sql(sql)
        ress = cusor.fetchall()
        return ress

    def get_unionid(self):
        sql = 'select distinct(unionid) from mf_schedule_personal order by id limit 200,100'
        cusor = SJJC_db.execute_sql(sql)
        res=cusor.fetchall()
        return res

    #从标签表,人物表,导入数据（测试）
    def data2_cardtable(self):
        name_list=list(map(lambda  x:x[0],self.get_name()))
        tag_list=list(map(lambda  x:x[0],self.get_tag()))
        unionid_list=self.get_unionid()
        for s in unionid_list:
            print(s[0])
            random.shuffle(tag_list)
            get_tag_info=random.sample(tag_list,random.randint(1,10))
            for tag in get_tag_info:
                Person_card_tagsModel.insert(name=name_list[unionid_list.index(s)],unionid=s[0],tag=tag,create_time=str(int(time.time()))).execute()
        print('数据导入成功！')

    def add_data(self,*args):
        pass
        # Person_card_tagsModel().create(name=args[0],tag=args[1])
        # print('add data ok!')
        # sql='insert into person_card_tag(name,uuid,tag) values(%s,%s,%s)'
        # self.model.insert()

    def get_data(self,n):
        pass
        # sql='select distinct(name) from mf_person_info where name is not null and name!="" order by id desc limit %s'%n
        # s=PersonModel().filter(PersonModel.name!='').order_by(fn.Rand()).limit(1)
        # print(s)
        # cusor=self.db.execute_sql(sql)
        # ress=cusor.fetchall()
        # for x in ress:
        #     if x:
        #         return x



def redis_main(data):
    r = redis.Redis(host='127.0.0.1',password='000000',port=6379,db=0)
    # redis = redis.StrictRedis.from_url('redis://@localhost:6379/0')
    # print(r.get('x'))
    for detail in data:
        print(detail)
        # data_lens=r.llen(detail[0].encode('utf8'))
        print(str(detail[0].encode('utf8')))
        data_lens=r.scard(detail[0])
        print(data_lens)
        # rece_data=r.lrange(detail[0],0,data_lens)
        # print('name:' + str(detail[0]))
        rece_data=r.smembers(detail[0])
        print(rece_data)
        if rece_data:
            # print('rece_data:',str(rece_data))
            # print(type(rece_data))
            print('info:')
            for x in rece_data:
                if x:
                    for z in x.split('|'):
                        print(z)
            # print('xueli:'+str(rece_data[0]['xueli']))
            # print('lingyu:'+str(rece_data['xueli']))
        else:
            for x in detail[1:]:
                r.sadd(detail[0],x)
                # r.lpush(detail[0],data)
                # r.set(detail[0],data)
            print('add ok!')

def type_swap(s):
    return s.encode('utf8') if isinstance(s,unicode) else s


class Data2Es_handle(object):

    def __init__(self):
        self.dest_host={
            "host":"10.30.51.108",
            "port":9200,
            "timeout": 10
        }
        self.host_info={
            'host': '127.0.0.1',
            'port': 9200
        }
        self.index='person_card'    #"person_test"
        self.doc_type="tags_info"
        # connection_pool = Transport(self.host_info, connection_class=RequestsHttpConnection).connection_pool
        # self.con=connection_pool.get_connection()
        # status, headers, data = con.perform_request('GET', '/' + ES_INDEX + '/_search?q=' + query)

        self.es = elasticsearch.Elasticsearch([self.host_info]) #host_info
        """
                    设置mapping
        """
        self.setting_s = {
            "settings": {
                # "number_of_shards": 1,
                # "number_of_replicas": 0,
                "analysis": {
                    "analyzer": {
                        "my_analyzer": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": ["lowercase"]
                        }}
                }
            },
            "mappings": {
                self.doc_type: {
                    "properties": {
                        "tags": {
                            "type": "text",
                            "fields": {
                                "default": {
                                    "type": "text",
                                    "analyzer": "standard"
                                },
                                "ik": {
                                    "type": "text",
                                    "analyzer": "ik_smart"
                                }
                            },
                            "analyzer": "my_analyzer"
                        }
                    }
                }
            }
        }
        if not self.es.indices.exists(index=self.index):
            try:
                create_index_flag = self.es.indices.create(index=self.index, body=self.setting_s, ignore=400)
                # create_mapping_flag=self.es.indices.put_mapping(index=self.index,doc_type=self.doc_type, body=setting_s)
                if create_index_flag["acknowledged"] == True:  # or create_mapping_flag["acknowledged"] != True:
                    # 创建Index和mapping
                    print('mapping ok!')
                else:
                    print('create failed!')
            except ElasticsearchException as e:
                print(e)
        else:
            print('index already exists!!')


    def get_data_away(self,id=None,input_tag=None):
        query = {
            "query": {
                "bool": {
                    "must_not": [
                        {
                            "match_phrase": {
                                "_id": ' '.join(id)
                            }
                        }
                    ],
                    "must": [
                        {
                            "match_phrase": {
                                "tags": ' '.join(input_tag)
                            }
                        }
                    ]
                }
            }
        }
        # status, headers, data = self.con.perform_request('GET', '/' + self.index+ '/_search?q=' + query)
        # print(data)

    def add_index(self):
        if self.es.indices.exists(index=self.index):
            try:
                dbs = Data_flow()
                for x in dbs.get_all_data():


                    # action = {
                    #     "_index": self.index,
                    #     "_type": self.doc_type,
                    #     "_source": {
                    #         "name": name,
                    #         "tag": tag
                    #     }
                    # }


                    doc = {
                    }
                    print(x[1])
                    doc['tags']=type_swap(x[1]).split(',')
                    doc['display_flag'] = x[2]

                    try:
                        self.es.create(index=self.index, doc_type=self.doc_type, id=type_swap(x[0]), body=doc)
                        print('data flow to es ok!')
                    except:
                        pass

            except ElasticsearchException as e:
                print(e)


        print('create doc ok!')

    #搜索匹配
    def query_es(self,input_tag,id_list,size,page):
        query={
            "highlight": {
                "fields": {
                    "tags": {}
                }
            },
            "query": {
                "bool": {
                  "must_not": [
                    {
                      "ids": {
                        "values": id_list
                      }
                    }
                  ],
                  "must": [
                    {
                      "match": {
                        "tags": ' '.join(input_tag)
                      }
                    }
                  ]
                }
            },
            "from":page-1,
            "size":size
            }

        result = self.es.search(
            index=self.index,
            doc_type=self.doc_type,
            sort={
                "_score": {
                    "order": "desc"
                }
            },
            body=query
        )
        print('result_lens:' + str(len(result['hits']['hits'])))
        # score={}
        # x=result['hits']['hits'][0]
        doc = []
        for x in result['hits']['hits']:
            id=x['_id']
            print('_score:'+str(x['_score']))
            source=x['_source']['tags']
        # #     score[x['_id']]=x['_source']['tags']
        # #     score[x['_id']]=x['_source']['tags']
            input_tag1=map(lambda x:type_swap(x),input_tag)
            tags_list=map(lambda x:(type_swap(x)).lower(),x['_source']['tags'] )
            count=0
            for x in tags_list:
                for y in input_tag1:
                    if re.findall('%s'%y,x):
                        count+=1
        #     print(count)
            cacl_rate=(float(count)/len(input_tag1)+random.random())*0.90
            print(cacl_rate)
            if cacl_rate>=0.0:
                doc.append([id,source,cacl_rate])

            # doc['source']=x['_source']
            # doc['score']=cacl_rate
        # print(doc)
        doc1 = sorted(doc, key=lambda x: x[-1], reverse=True)

        print(doc1)
        print(len(doc1))
            # return  score


    #年龄，地域
    def search2es(self,age,area=None,job=None):
        if self.es.indices.exists(index=self.index):
            result=self.es.search(
                index=self.index,
                # q='http_status_code:5*"',
                size=10,
                doc_type=self.doc_type,
                # search_type='scan',
                sort={
                        "_score": {
                            "order": "desc"
                        }
                    },
                body={
                        "query": {
                            "bool":{
                                "filter": {
                                    "range": {
                                        "年龄":  {
                                            "gte":"%d"%age
                                            }
                                        },
                                },
                            "must":{
                                "match": {
                                    "地域": "%s"%area
                                },
                            },
                            "should": {
                                "match": {
                                    "职业": "%s" % job
                                },
                            }
                        }
                    },
                }
            )
            print('result_lens:'+str(len(result['hits']['hits'])))
            for x in result['hits']['hits']:
                print(x["_source"])

    def add_bigdata2es(self):
        # self.es.bulk()
        pass
    def update_by_id(self, row_obj):
        """
        根据给定的_id,更新ES文档
        """
        _id = row_obj.get("_id", 1)
        row_obj.pop("_id")
        self.es.update(index=self.index, doc_type=self.doc_type, body={"doc": row_obj}, id=_id)

    def del_index_doc(self):
        pass

def tags_product():
    with open('/Users/qmp/Desktop/mock.txt','r') as f:
        data=f.readlines()
    print(type(data))
    print(len(data))
    data=map(lambda x:x.decode("utf8"),data)
    # print(data)
    # # for i in s:
    # #     print(len(i))
    # #     for j in i:
    # #         print(j)
    with open('/Users/qmp/Desktop/tags.txt','w+') as f:
        for _ in range(70):
            f.writelines(str(random.sample(data,random.randrange(5,21))))
    print('ok!')


if __name__ == '__main__':
    # dbs=Data_flow()
    # dbs.data2_cardtable()
    # redis_main()
    # es=Data2Es_handle()
    # es.add_index()
    # tag_list=['游戏','玻璃','美业','LBS','智能','机器人','app']
    # id_list=["oP3fkwDdHoSBnzrMNvJIIAGNVyFQ","oP3fkwKJnlRD5T74TZKEbUzJn5Eo","oP3fkwDJyd7F8ZOFDAIgJUUbVrr4"]
    # ress=es.query_es(tag_list,id_list,10,1)
    tags_product()









    """
    测试预运行
    """
    # items_list = ['年龄', '职业', '地域']
    # name_list = ['sam', 'john', 'mate', 'jack', 'tim', 'jerry', 'harry']
    # age_list = [30, 25, 33, 24, 33, 34, 45]
    # job_list = ['司机', '木匠', '园丁', '教师', '司机', '消防员', '医生']
    # area_list = ['新疆', '云南', '北京', '北京', '深圳', '辽宁', '上海']
    # for i in range(len(name_list)):
    #     data =dict(zip(items_list,[age_list[i],job_list[i],area_list[i]]))
    #     es.create_data2es(name_list[i],data)
    # fix_data =  {
    #     "_id": "%s",
    #     "document_id": 1,
    #     "title": u"Hbase 测试数据",
    #     "content": u"Hbase 日常运维,这是个假数据监控Hbase运行状况。通常IO增加时io wait也会增加，现在FMS的机器正常情况......",
    # }
    #
    # es.search2es(age=24,area='北京',job='')
