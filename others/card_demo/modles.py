#coding:utf8

from peewee import *
from playhouse.shortcuts import RetryOperationalError
class RetryMySQLDatabase(RetryOperationalError, MySQLDatabase):
    pass

SJJC_db = RetryMySQLDatabase('xx',
                           **{
                              })


class BaseModel(Model):
    class Meta:
        database = SJJC_db


#人物名片标签表
class Person_card_tagsModel(BaseModel):
    id=IntegerField(primary_key=True)
    name = CharField(index=True, null=True)
    unionid = CharField(index=True, null=True)
    tag = CharField(index=True, null=True)
    create_time = CharField(index=True, null=True)
    class Meta:
        db_table = 'person_card_tags'

class PersonModel(BaseModel):
    id = IntegerField(null=True)
    icon = CharField(null=True)
    name = CharField(null=True)
    ename = CharField(null=True)
    jieshao = CharField(null=True)
    update_time = DateTimeField(null=True)
    display_flag = IntegerField(null=True)

    class Meta:
        db_table = 'mf_person_info'

tables_list=[Person_card_tagsModel]
SJJC_db.connect()
SJJC_db.create_tables(tables_list, safe=True)
