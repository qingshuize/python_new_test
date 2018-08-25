#_*_ coding:utf-8 _*_
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import re
import itchat
import time
from itchat.content import *
import random
import requests

ITEM_LIST=[u'苟利',u'苟利国家生死以，岂因祸福避趋之',u'人在做，天在看',u'大学之道，在明明德',u'量小非君子，无毒不丈夫',u'大江歌罢掉头东，邃密群科济世穷。面壁十年图破壁，难酬蹈海亦英雄。',u'神女应无恙，当惊世界殊。',u'雄关漫道真如铁，而今迈步从头越',u'昔我往矣，杨柳依依。今我来思，雨雪霏霏。',u'硕鼠硕鼠，无食我黍',u'安能摧眉折腰事权贵，使我不得开心颜！',u'我心伤悲，莫知我哀',
           u'我无所谓！',u'图样图森破',u'上台拿衣服',u'月上柳梢头，人约黄昏后。',u'落花人独立，微雨燕双飞。',u'苟日新，日日新。',u'苟富贵，勿相忘。',u'待到秋来九月八，我花开后百花杀。冲天香阵透长安，满城尽带黄金甲。',u'岁寒，然后知松柏之后凋也。',u'穷且益坚，不坠青云之志',u'周公吐哺，天下归心。',u'山不厌高，海不厌深。',u'榆柳荫后檐，桃李罗堂前。','放弃幻想，准备战斗!','你说哈哈哈，我想呵呵呵',
           '非淡泊无以明志，非宁静无以致远','仓廪实而知礼节，衣食足而知荣辱','小时了了，大未必佳','未若柳絮因风起','运筹帷幄之中，决胜千里之外','饿死事小，失节事大。','To be, or not to be, that is a question.','Give me liberty, or give me death!','Je pense, donc je suis.','I think, therefore I am.',
           ]



@itchat.msg_register([TEXT, MAP, NOTE, SHARING])
def text_reply(msg):
    # print(msg)
    friend = itchat.search_friends(userName=msg['FromUserName'])
    # print(friend)
    print(msg['Type'])
    if friend['NickName'] in [u'x',u'xx']:
        if msg['Type'] in ['Text','Note']:
            info=msg['Content'].replace(' ','').encode('utf8')
            if not re.findall(r"(傻|sb|SB|煞笔)", info):
                random.shuffle(ITEM_LIST)   #列表顺序打乱处理
                return '%s  %s\n ~~ %s' % (msg['Text'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),random.choice(ITEM_LIST))
                # msg.user.send('%s: %s' % (msg.type, msg.text))
            else:
                return '哎呦，要好好说话'

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    print(msg)
    name=msg.get('ActualNickName')
    print(name)
    # if name in [u'56666',u'hola']:
    #     if msg.ActualNickName!=u'Van.ziran':
    #         random.shuffle(ITEM_LIST)
    #
    #         msg.user.send(u'@%s 回复: %s @@%s' % (
    #             msg.actualNickName, msg.text,random.choice(ITEM_LIST)))
    #         print(msg.actualNickName)
    #         print(msg.text)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO, NOTE])
def Reply_media(msg):
    friend = itchat.search_friends(userName=msg['FromUserName'])
    # print(friend)
    print(msg['Type'])
    content=msg.get(u'Content')
    url=re.findall(r'cdnurl="(.*)"designerid',content.replace(' ',''))[0]
    print(url)
    if friend['NickName'] in [u'x',u'xx']:
        filename=msg.get(u'MsgId')+'.png'
        res=requests.get(url)
        with open(filename,'w') as f:
            f.write(res.content)
        print('save ok!')
        typeSymbol = {
            PICTURE: 'img',
            VIDEO: 'vid', }.get(msg['Type'], 'fil')
        return '@%s@%s' % (typeSymbol, filename)
        # msg.download(msg.fileName)
        #读取二进制文件，不下载
        # msg.download(msg.fileName)
        # typeSymbol = {
        #     PICTURE: 'img',
        #     VIDEO: 'vid', }.get(msg.type, 'fil')
        # return '@%s@%s' % (typeSymbol, msg.fileName)



def start():
    print('finish login')
def end():
    print('exit')

# @itchat.msg_register(CARD)
# def get_friend(msg):
#     if msg['ToUserName'] == 'filehelper':
#         print msg
#         # print(msg['RecommendInfo'])
#         friendStatus = get_friend_status(msg['RecommendInfo'])
#         itchat.send(friendStatus['NickName'], 'filehelper')


##微信控制器
import subprocess
from NetEaseMusicApi import interact_select_song

def open_music():
    subprocess.call(["open", 'stop.mp3'])

def close_music():
    # os.startfile('stop.mp3') #windows os
    subprocess.call(["open", 'stop.mp3'])

# @itchat.msg_register(TEXT)
# def music_player(msg):
#     try:
#         if msg['ToUserName']== 'filehelper':
#             if msg['Text'] == u'关闭':
#                 close_music()
#                 itchat.send(u'音乐已关闭', 'filehelper')
#             elif msg['Text'] == u'帮助':
#                 itchat.send(u'帮助信息...', 'filehelper')
#             else:
#                 select_info=interact_select_song(msg['Text'])
#                 itchat.send(select_info, 'filehelper')
#                 print(select_info)
#
#     except Exception as e:
#         print(e)


# def test_friend():
#     chatroomUserName = '@1234567'
#     friend = itchat.get_friends()[1]
#     print friend
#     r = itchat.add_member_into_chatroom(chatroomUserName, [friend])
#     if r['BaseResponse']['ErrMsg'] == '':
#         status = r['MemberList'][0]['MemberStatus']
#         itchat.delete_member_from_chatroom(chatroom['UserName'], [friend])
#         return { 3: u'该好友已经将你加入黑名单。',
#             4: u'该好友已经将你删除。', }.get(status,
#             u'该好友仍旧与你是好友关系。')
#

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
    time.sleep(1)
    itchat.run()
    itchat.logout()
    # test_friend()
