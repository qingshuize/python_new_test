#coding:utf8
from flask import Flask,jsonify,request

app=Flask(__name__)

@app.route('/',methods=['GET'])
def Index():
    return 'haha'

@app.route('/query_result/<unionid>/<tag_list>',methods=['POST'])
def Get_search_result(id,tag_list):
    id=request.f



if __name__ == '__main__':
    try:
        app.run(debug=True,
                host='127.0.0.1',
                port=7722,
                threaded=True,
                processes=0,
                use_debugger=True,
                use_reloader=True)
    except Exception as e:
        print(e)

