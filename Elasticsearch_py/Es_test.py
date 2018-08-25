#coding:utf8
from elasticsearch import helpers
from peewee import *
from playhouse.shortcuts import RetryOperationalError
from config import es
from elasticsearch.helpers import BulkIndexError


class RetryMySQLDatabase(RetryOperationalError, MySQLDatabase):
    pass


mysql={
    'shujujiance':{
        'host': '127.0.0.1',
        'password': '123456',
        'port': 3306,
        'user': 'root',
        "database": '',
    }

}

def sql2dicts(db, sql):
    """
    注意: 每次返回若干个dic而不是一个。这样方便批量插入es
    """
    offset = 0
    size = 1000
    sql = sql + " limit %s, %s"
    while True:
        cursor = db.execute_sql(sql, (offset, size))
        if not cursor.rowcount:
            break
        fieldnames = [field[0] for field in cursor.description]
        dics = [dict(zip(fieldnames, tuple_)) for tuple_ in cursor]
        yield dics
        offset += size


def mysql2es_handle(sql, database_id, index_, doctype, fieldtypes, is_insert, func):
    if is_insert is None:
        is_insert = False
    db = RetryMySQLDatabase(
        mysql,
        **{k: v for k, v in mysql.items() if k != "database"}
    )
    for dics in sql2dicts(db, sql):
        docs = list()
        for dic in dics:
            if func:
                func_ = getattr(functions, func)
                dic = func_(**dic)
                # print dic

            for k, v in fieldtypes.items():
                if v == "list":
                    dic[k] = [v.strip() for v in dic[k].split(",") if v.strip()] if dic[k] else []

            _id = dic["_id"]
            del dic["_id"]

            docs.append({
                '_id': _id,
                "_type": doctype,
                "_index": index_,
                "_source": {
                    'doc': dic,
                    'doc_as_upsert': True
                },
                '_op_type': 'update',
            })


        if is_insert:
            helpers.bulk(es, docs)
        else:
            try:
                helpers.bulk(es, docs)
            except BulkIndexError as e:
                print(e)


if __name__ == '__main__':
    sql='select title,description,post_time from totalnews limit 100'
    mysql2es_handle(sql,None)
