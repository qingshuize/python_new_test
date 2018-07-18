#coding:utf8
import re,sys,json
import urllib2
import requests
from peewee import *

mysql_db = MySQLDatabase(
###
)

def try_except(func):
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            print(e)
    return wrapper

@try_except
def select_info():
    sql = 'select title,post_time from totalnews where product_like is not null and financing_round is not null and financing_amount is not null limit 10000'
    cur = mysql_db.execute_sql(sql)
    result = cur.fetchall()
    for x in result:
        title = x[0]
        title = title.encode('utf8')
        time = x[1]
        if '融资' in title:
            yield title
        else:
             pass

@try_except
def translate(text,origin,new):
    # text 输入要翻译的句子
    text_1 = text
    headers={
        'authority':'translate.google.cn',
        #':authority:translate.google.cn
        #':path':'/',
        # ':scheme':'https',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie':'NID=119=ioNaCzEJx5NingWBWDxKKj-3aV5pEWlW8GB32zLuI17MyOOqdFzQfxpEjgxp4pB6xNA28texn_R6JIhlQiMR8orN6mPCT7iLiI_rGycTb24uyOOZBGY6FfSFRCc7Nsyd; _ga=GA1.3.1137876970.1513915995; _gid=GA1.3.1860578888.1513915995; 1P_JAR=2017-12-22-4',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'x-client-data':'CJK2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQjtnsoBCKijygE='
    }
    # so='3' if origin=='zh-CN' else '0'
    # kc = '1' if origin == 'zh-CN' else '0'
    # tt = '846595.688567' if origin == 'zh-CN' else '634268.1034024'
    data='client=t&sl=%s&tl=%s&hl=%s&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=5&tk=173863.314782&q=%s'%(origin,new,origin,urllib2.quote(text_1))
    url = 'http://translate.google.cn/translate_t'
    #url='https://translate.google.cn/translate_a/single'
    res=requests.get(url,params=data)
    html=res.text
    # raw_info=json.loads(html)
    # text_2=raw_info[0][0][0]
    #p = re.compile(r"(?<=TRANSLATED_TEXT=).*?;")
    #m = p.search(html)
    #text_2 = m.group(0).strip(';')
    text_2 = re.findall(r"TRANSLATED_TEXT='(.*)';var ctr",html)[0]
    return text_2

@try_except
def text_handle(text):
    vital_words=['financing','investment','money','round','Financing']
    com_words=['company','']
    invest_com=['Oriental']
    rounds_words_list=['round','investment','Financing']
    number_words=['million','Million','millions','billion','billions']
    unit_words=['dollars','euros','$']
    #rounds_index=re.search('%s'%x,text)[0]
    vital_iter=iter(vital_words)
    final_result=[]
    while True:
        try:
            vital_item=vital_iter.next()
            if vital_item in text:
                #轮次
                for rounds_words in rounds_words_list:
                    if rounds_words in text:
                        rounds_index=text.index(rounds_words)
                        rounds=text[:rounds_index].strip().split(' ')[-1]
                        if rounds=='+':
                            rounds=text[:rounds_index].strip().split(' ')[-2]+rounds
                        rounds=rounds+' '+rounds_words
                        print('rounds:'+rounds)
                        rounds_2 = translate(rounds, 'en','zh-CN').strip("'")
                        print('轮次:%s' % rounds_2.encode('utf8').replace(' ',''))
                        final_result.append(rounds_2)
                        break



                #货币单位
                unit=''
                for x in unit_words:
                    unit=x if x in text else unit


                #数额
                number_inter=iter(number_words)
                try:
                    if unit:
                        numbers_index = text.index(unit)
                        if unit!='$':
                            numbers = ' '.join(text[:numbers_index].strip().split(' ')[-3:])
                        else:
                            numbers = text[numbers_index+1:].strip().split(' ')[0]
                            unit='dollars'
                        numbers = numbers + ' ' + unit

                        print(numbers)
                        numbers_2 = translate(numbers, 'en', 'zh-CN').strip("'")
                        print('数额:%s' % numbers_2.encode('utf8'))
                        final_result.append(numbers_2)
                        break

                    else:
                        while True:
                            x=number_inter.next()
                            if x in text:
                                numbers_index=text.index(x)
                                numbers = ' '.join(text[:numbers_index].strip().split(' ')[-2:])+' '+x
                                numbers=numbers+' '+unit
                                print(numbers)
                                numbers_2 = translate(numbers, 'en', 'zh-CN').strip("'")
                                print('数额:%s' % numbers_2.encode('utf8'))
                                final_result.append(numbers_2)
                                break


                except Exception as e:
                    print(e)
                print('len:',len(final_result))
                return len(final_result)

                break
        except Exception as e:
            print(e)
            break








if __name__ == "__main__":
    # text_1 = ','.join(sys.argv[1:])
    i=0
    j=0
    for detail in select_info():
        text_1=detail
        i+=1
        #text_1=text_1.replace('“','"') if '“' in text_1 else text_1
        text_1 = text_1.replace('“', '').replace('”', ' ').replace(' ','')
        print('%s' % text_1.decode('utf8'))
        text_2 = translate(text_1,'zh-CN','en')
        print('%s' % text_2)
        j+=1 if text_handle(text_2)>=1 else 0
    print('total_sum:'+str(i))
    print('real_num:'+str(j))
