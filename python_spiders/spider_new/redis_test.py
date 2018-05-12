#coding:utf8
import redis
import time
def redis_test():
    #r=redis.StrictRedis(host='127.0.0.1',port=6379)
    r=redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)

    print(r.lrange('list_test',1,20))
    for i in ['q','w','e','r']:
        # r.rpush('list_test',i)

        r.lpop('list_test')
    print(r.lrange('list_test', 1, 20))
    # pipe = r.pipeline(transaction=True)
    # name=r.get('name')
    # print(type(eval(name)))
    # print(name)
    # r.set('age',29)
    # print(type(eval(r.get('age'))))
    # time.sleep(2)
    # pipe.execute()


    #事务
    # try:
    #     # pipe.watch('a')
    #     pipe.multi()
    #     pipe.set('here', 'there')
    #     pipe.set('here1', 'there1')
    #     pipe.set('here2', 'there2')
    #     time.sleep(5)
    #     pipe.execute()
    #
    # except redis.exceptions.WatchError as e:
    #     print("Error")

if __name__ =="__main__":
    redis_test()