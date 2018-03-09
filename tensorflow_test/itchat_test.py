#_*_ coding:utf-8 _*_
import re
import itchat
import time
from itchat.content import *
import random

ITEM_LIST=[u'苟利',u'苟利国家生死以，岂因祸福避趋之',u'人在做，天在看',u'大学之道，在明明德',u'量小非君子，无毒不丈夫',u'大江歌罢掉头东，邃密群科济世穷。面壁十年图破壁，难酬蹈海亦英雄。',u'神女应无恙，当惊世界殊。',u'雄关漫道真如铁，而今迈步从头越',u'昔我往矣，杨柳依依。今我来思，雨雪霏霏。',u'硕鼠硕鼠，无食我黍',u'安能摧眉折腰事权贵，使我不得开心颜！',u'我心伤悲，莫知我哀',
           u'我无所谓！',u'图样图森破',u'上台拿衣服',u'月上柳梢头，人约黄昏后。',u'落花人独立，微雨燕双飞。',u'苟日新，日日新。',u'苟富贵，勿相忘。',u'待到秋来九月八，我花开后百花杀。冲天香阵透长安，满城尽带黄金甲。',u'岁寒，然后知松柏之后凋也。',u'穷且益坚，不坠青云之志'
           ]

# @itchat.msg_register([TEXT])
# def text_reply(msg):
#     friend = itchat.search_friends(userName=msg['FromUserName'])
#     replyContent = "收到您于%s发送的【%s】" % (time.strftime('%m-%d %H:%M',time.localtime()), msg['Type'])
#     # if msg['Type'] == 'Text':
#     #     if re.search(r"快乐",msg['Content']):
#     #         replyContent += "【衷心感谢您的祝福,祝您：新年快乐😊😊😊,开开心心[耶][耶][耶],身体健康[發][發][發],狗年大吉旺旺旺🐶🐶🐶】"
#     #         itchat.send('@img@%s' % '/Users/qmp/Desktop/timg.jpeg',toUserName=msg['FromUserName'])
#
#     # itchat.send(msg['Text'].encode('utf8'),toUserName='filehelper')
#     # itchat.send("好友:【%s（昵称：%s）】于：【%s】发来消息: 【%s】" % (friend['NickName'], friend['RemarkName'], time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), msg['Text']),toUserName='filehelper')
#     print(type(msg['Text']))
#     itchat.send("发来消息: 【%s】" % msg['Text'],toUserName='filehelper')
#     # itchat.send(replyContent,toUserName=msg['FromUserName'])
#     print("于【%s】收到好友【%s（昵称：%s）】发来的【%s】: 【%s】" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), friend['NickName'], friend['RemarkName'], msg['Type'], msg['Content']))
#     # print("于【%s】回复：%s" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), replyContent)+'\n')
# itchat.auto_login(hotReload=True)
# itchat.run()


# def chat_test():
#     try:
#         itchat.auto_login(hotReload=True)
#         i=1
#         while i<4:
#             itchat.send('Hello, filehelper,this is %s times'%i, toUserName='filehelper')
#             i+=1
#     except Exception as e:
#         print(e)
#
@itchat.msg_register([TEXT, MAP, NOTE, SHARING])
def text_reply(msg):
    friend = itchat.search_friends(userName=msg['FromUserName'])
    print(friend)
    print(msg['Type'])
    if friend['NickName'] in [u'飘荡在北方', u'Phantom']:
        if msg['Type'] in ['Text','Note']:
            info=msg['Content'].encode('utf8').replace(' ','')
            if not re.findall(r"刘樊是[傻|sb|SB]", info):
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
    # if not msg.IsAt:
    # # if msg['NickName'] in [u'最高三人团']:
    #     print(u'%s send message,I received: %s' % (msg.actualNickName, msg.text))
    #     msg.user.send(u'%s send message,I received: %s' % (
    #         msg.actualNickName, msg.text))

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO,NOTE])
def Reply_media(msg):
    friend = itchat.search_friends(userName=msg['FromUserName'])
    print(friend)
    print(msg['Type'])
    if friend['NickName'] in [u'飘荡在北方',u'Phantom']:
        # msg.download(msg.fileName)
        #读取二进制文件，不下载
        msg.download(msg.fileName)
        typeSymbol = {
            PICTURE: 'img',
            VIDEO: 'vid', }.get(msg.type, 'fil')
        return '@%s@%s' % (typeSymbol, msg.fileName)
        # itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']),msg['FromUserName'])
        # return '%s received' % msg['Type']
        # print msg.download()
        # with open(msg.fileName,'wb') as f:
        #     f.write(msg.download)
        #


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
#     chatroomName=u'最高三人团'
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