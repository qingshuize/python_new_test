#coding:utf8
from elasticsearch import Transport
from elasticsearch.connection import RequestsHttpConnection
import json
import time

dest_host={
            "host":'127.0.0.1',
            "port":9200,
            "timeout": 10
        }
ES_INDEX='person_card'    #"person_test"
ES_TYPE="tags_info"
connection_pool = Transport(dest_host, connection_class=RequestsHttpConnection).connection_pool
con=connection_pool.get_connection()
input_tag=''
# query = {
#             "query": {
#                 "bool": {
#                     "must_not": [
#                         {
#                             "match_phrase": {
#                                 "_id": ' '.join(id)
#                             }
#                         }
#                     ],
#                     "must": [
#                         {
#                             "match_phrase": {
#                                 "tag": ' '.join(input_tag)
#                             }
#                         }
#                     ]
#                 }
#             }
#         }
keyword='123'
page_size=5
page=2
query_str="""
{
  "highlight": {
    "fields": {
      "tags": {
      }
    }
  },
  "sort": [{"_score": {"order": "desc"}}],
  "query": {
    "bool": {
      "must_not": [
        {
          "ids":{
            "values": ["oP3fkwDdHoSBnzrMNvJIIAGNVyFQ","oP3fkwKJnlRD5T74TZKEbUzJn5Eo","oP3fkwDJyd7F8ZOFDAIgJUUbVrr4"]

          }}
        ],
        "must": [
          {"match":
          {"tags": "游戏 玻璃 美业 LBS 智能 机器人 app"

          }}]}},

}
"""
query_str = "((tag:*"+keyword+"*))AND(is_public:true)AND(publish_time:[0 TO "+str(int(time.time()))+"])"
query_str += "&size=" + str(page_size)
query_str += "&from=" + str((page - 1) * page_size)

status, headers, data = con.perform_request('GET', '/' + ES_INDEX + '/'+ES_TYPE+'/_search?q=' + str(query_str))
res = json.loads(data)
