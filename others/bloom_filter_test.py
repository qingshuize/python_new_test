#coding:utf8
class Bloom_test(object):
    def __init__(self):
        self.len=11
        self.origin_index=[i for i in range(self.len+1)]
        self.origin_value=[0 for _ in range(self.len+1)]
        self.origin_dict=dict(zip(self.origin_index,self.origin_value))

    def get_origin(self):
        return self.origin_dict

    def create_filter(self,s):
        s_bin=bin(s)[2:]
        print(s_bin)
        s_x=[s_bin[len(s_bin)-i] for i in range(len(s_bin),0,-1) if i%2==0]
        s_y=[s_bin[len(s_bin)-i] for i in range(len(s_bin),0,-1) if i%2!=0]
        s_x_bin=''.join(s_x)
        s_y_bin=''.join(s_y)
        flag_list=[]
        print(s_x_bin)
        x_dec=int(s_x_bin,2)
        y_dec = int(s_y_bin, 2)
        print('bin x:',x_dec)
        bit_x_flag=x_dec%self.len
        # print('bit_x_flag:',bit_x_flag)
        flag_list.append(bit_x_flag)
        print(s_y_bin)
        print('bin y:',y_dec)
        bit_y_flag = y_dec % self.len
        flag_list.append(bit_y_flag)
        # print('bit_y_flag:', bit_y_flag)
        decry_dict=self.origin_dict
        for x in flag_list:
            decry_dict[x]=1
        print('decrypt list:')
        print(decry_dict)




if __name__ == '__main__':
   b_s= Bloom_test()
   print(b_s.get_origin())
   b_s.create_filter(120)