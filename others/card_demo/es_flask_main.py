#coding:utf8
from flask import Flask,request,jsonify
app = Flask(__name__)
import requests
import time
import logging
import random
import json,re


@app.route('/',methods=['GET'])
def Index_page():
    return 'hahah'

def type_swap(s):
    return s.encode('utf8') if isinstance(s,unicode) else s

@app.route('/search',methods=['POST'])
def Person_card_search():
    raw_unionid_list = (request.form.get("unionid_list", type=str, default=""))
    unionid_list = raw_unionid_list.split('|') if raw_unionid_list  else []
    print(unionid_list)
    input_tags = (request.form.get("tags_list", type=str, default="")).replace('|',' ')
    print(input_tags)
    # #显示第几页，从1开始
    page_n = request.form.get("page_n", type=int, default=1)-1 if request.form.get("page_n")>0 else 0
    # #每页显示xx条结果
    size = request.form.get("size", type=int, default=20) if request.form.get("size")>=0 else 0
    if input_tags:
        must_query=[
            {
                "match": {
                    "tags.ik": input_tags
                }
            },
            {
                "match": {
                    "display_flag": 1  # 1表示展示
                }
            }
        ]

    else:
        must_query=[
            {
                "match": {
                    "display_flag": 1  # 1表示展示
                }
            }
        ]
    query = {
        "highlight": {
            "fields": {
                "tags": {},
                "tags.ik": {}
            }
        },
        "query": {
            "bool": {
                "must_not": [
                        {
                    "ids": {
                        "values": unionid_list
                            }
                        }
                ],
                "must":
                    must_query
        }
        },
        "from":page_n,
        "size":size,
        "sort": [{"_score": {"order": "desc"}}]
    }
    start_time = time.time()
    try:
        headers={
            "Content-Type": "application/json"
        }
        resp = requests.post(
            url=random.choice([
                "http://127.0.0.1:9200/person_card/tags_info/_search",
                # "http://10.30.50.229:9200/person_card/tags_info/_search"
            ]),
        data=json.dumps(query),headers=headers)

    except Exception as e:
        print(e)
        return 'Internal Error!'
    logging.info("查询耗时%f秒" % (time.time() - start_time))
    # print(resp.content)
    return resp.content
    # result=json.loads(resp.content)
    # if must_query:
    #     data = result.get('hits').get('hits')
    #     doc1 = []
    #     if data:
    #         for i in range(len(data)):
    #             input_tags1 = map(lambda x: type_swap(x), input_tags.split(' '))
    #             own_tags = map(lambda x: (type_swap(x)).lower(), data[i]['_source']['tags'])
    #             count = 0
    #             for x in own_tags:
    #                 for y in input_tags1:
    #                     if x==y:
    #                         count+=1
    #                     else:
    #                         if re.findall('%s' % y, x):
    #                             count += 0.5
    #             cacl_rate=1.0
    #             while cacl_rate>=1:
    #                 rate= 0.99 if float(count) / len(input_tags1) >=1.0 else float(count) / len(input_tags1)
    #                 cacl_rate = rate
    #                 # cacl_rate = (rate + random.random()*0.1) * 0.90
    #             ##「我的标签」小于等于3个的用户，在结果匹配度基础上*50%
    #             if len(own_tags)<=3:
    #                 cacl_rate=cacl_rate*0.5
    #             print('cacl_rate:'+str(cacl_rate))
    #             if cacl_rate >0.0:
    #                 data[i]['_score']=cacl_rate
    #         doc1 = sorted(data, key=lambda x: x['_score'], reverse=True)
    #         # print(doc1)
    #     result['hits']['hits'] = doc1
    #
    # return jsonify(result)

if __name__ == '__main__':
    app.run(host="127.0.0.1",
            debug=True,
            threaded=True,
            processes=0,
            use_debugger=True,
            use_reloader=True,
            port=5002)
    # app.run(host=localhosts, debug=False, port=5002)