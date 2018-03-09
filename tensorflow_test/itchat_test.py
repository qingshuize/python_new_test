#_*_ coding:utf-8 _*_
import re
import itchat
import time
from itchat.content import *
import random

ITEM_LIST=[u'苟利',u'苟利国家生死以，岂因祸福避趋之',u'人在做，天在看',u'大学之道，在明明德',u'量小非君子，无毒不丈夫',u'大江歌罢掉头东，邃密群科济世穷。面壁十年图破壁，难酬蹈海亦英雄。',u'神女应无恙，当惊世界殊。',u'雄关漫道真如铁，而今迈步从头越',u'昔我往矣，杨柳依依。今我来思，雨雪霏霏。',u'硕鼠硕鼠，无食我黍',u'安能摧眉折腰事权贵，使我不得开心颜！',u'我心伤悲，莫知我哀',
           u'我无所谓！',u'图样图森破',u'上台拿衣服',u'月上柳梢头，人约黄昏后。',u'落花人独立，微雨燕双飞。',u'苟日新，日日新。',u'苟富贵，勿相忘。',u'待到秋来九月八，我花开后百花杀。冲天香阵透长安，满城尽带黄金甲。',u'岁寒，然后知松柏之后凋也。',u'穷且益坚，不坠青云之志'
           ]



@itchat.msg_register([TEXT, MAP, NOTE, SHARING])
def text_reply(msg):
    friend = itchat.search_friends(userName=msg['FromUserName'])
    print(friend)
    print(msg['Type'])
    if friend['NickName'] in [u'xxx',]:
        if msg['Type'] in ['Text','Note']:
            info=msg['Content'].encode('utf8').replace(' ','')
            if not re.findall(r"[傻|sb|SB]", info):
                return '|---> |--->%s %s\n %s' % (msg.text, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),random.choice(ITEM_LIST))
                # msg.user.send('%s: %s' % (msg.type, msg.text))

@itchat.msg_register(itchat.content.FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')

@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    print msg
    print(type(msg))
    print msg.ActualNickName
    print msg.User
    if msg.ActualNickName:
        print(msg.text)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO,NOTE])
def Reply_media(msg):
    friend = itchat.search_friends(userName=msg['FromUserName'])
    print(friend)
    print(msg['Type'])
    if friend['NickName'] in [u'xxx',u'Phantom']:
        # msg.download(msg.fileName)
        #读取二进制文件，不下载
        msg.download(msg.fileName)
        typeSymbol = {
            PICTURE: 'img',
            VIDEO: 'vid', }.get(msg.type, 'fil')
        return '@%s@%s' % (typeSymbol, msg.fileName)



def start():
    print('finish login')
def end():
    print('exit')

@itchat.msg_register(itchat.content.CARD)
def get_friend(msg):
    if msg['ToUserName'] != 'filehelper':
        return
    print(msg['RecommendInfo'])
    # friendStatus = get_friend_status(msg['RecommendInfo'])
    # itchat.send(friendStatus['NickName'], 'filehelper')


# @itchat.msg_register([TEXT])
# def Room_replay():
#     REAL_SINCERE_WISH = u'祝%s新年快乐！！'
#     chatroomName=u'xxxx'
#     itchat.get_chatrooms(update=True)
#     chatrooms = itchat.search_chatrooms(name=chatroomName)
#     if chatrooms is None:
#         print(u'没有找到群聊：' + chatroomName)
#     else:
#         chatroom = itchat.update_chatroom(chatrooms[0]['UserName'])
#         for friend in chatroom['MemberList']:
#             friend = itchat.search_friends(userName=friend['UserName'])
#             # 如果是演示目的，把下面的方法改为print即可
#             print (REAL_SINCERE_WISH % (friend['DisplayName']
#                 or friend['NickName']), friend['UserName'])
#             itchat.send(REAL_SINCERE_WISH % (friend['DisplayName']
#                 or friend['NickName']), friend['UserName'])
#             # time.sleep(.5)


if __name__ =='__main__':
    itchat.auto_login(loginCallback=start, exitCallback=end)
    time.sleep(3)
    itchat.run()
