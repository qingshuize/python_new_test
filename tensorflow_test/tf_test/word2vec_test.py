#coding:utf8
import tensorflow as tf
import os
import random
import zipfile
import math
import requests
import collections

path='/Users/qmp/Desktop/'
def readfile(filename,size):
    if os.path.exists(path+filename):
        if os.path.getsize(path+filename)==size:
            with zipfile.ZipFile(path+filename) as zf:
                data=tf.compat.as_str(zf.read(zf.namelist()[0])).split()
            return data
        else:
            print('file size error!!!')
    else:
        url='http://mattmahoney.net/dc/text8.zip'
        rs=requests.get(url)
        with open(path+filename,'w') as f:
            f.write(rs.content)
        print('save ok!')



def Word2Vec():
    top_number=1000
    word=readfile('text8.zip',31344016)
    print('word size:'+str(len(word)))

    #collections.Counter()统计单词列表中单词频数
    #most_comment(N) 统计出出现频数前N的单词
    count=[['UNK',-1]]
    count.extend(collections.Counter(word).most_common(top_number-1))

    dic={}
    for x,_ in count:
        dic[x]=len(dic)

    data=[]
    unk_count=0
    for w in word:
        if w in dic:
            index=dic[w]
        else:
            index=0
            unk_count+=1
        data.append(index)
    count[0][1]=unk_count
    reverse_dic=dict(zip(dic.values(),dic.keys()))
    # print(data)
    print(count)
    print(dic)
    # print(reverse_dic)
    del word
    print('most:',count[:5])
    print('sample data:',data[:10],[reverse_dic[i] for i in data[:10]])



if __name__=='__main__':
    Word2Vec()