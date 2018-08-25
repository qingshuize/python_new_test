#coding:utf8
from elasticsearch import Elasticsearch

localhosts=[
    {
        'host':'127.0.0.1',
        'port': 9200
    }
]
onlinehosts = [
    # {"host": "10.30.51.108", "port": 9200},
    # {"host": "10.30.50.229", "port": 9200},
]

localhost = "127.0.0.1"
alihost = ""

is_test = True
if is_test:
    hosts = localhosts
    serverhost = localhost
else:
    hosts = onlinehosts
    serverhost = alihost

es=Elasticsearch(hosts)