#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import itchat

itchat.auto_login()

itchat.send('Hello, filehelper', toUserName='filehelper')