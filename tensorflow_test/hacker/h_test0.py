#coding:utf8
import crypt
import string
path='/Users/qmp/Desktop/'
def test(info):
    salt=info[0:2]
    word_dict=[x for x in (string.digits+string.letters)]
    for word in word_dict:
        cryptword=crypt.crypt(word,salt)
        if cryptword==info:
            print('ok!passwd:%s'%word)




def main():
    with open(path+'user.txt','r') as f:
        for line in f.readlines():
            if ':' in line:
                user=line.split(':')[0].strip()
                print(user)
                passwd=line.split(':')[1].strip()
                test(passwd)




if __name__=='__main__':
    main()