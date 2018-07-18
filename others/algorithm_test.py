#coding:utf8
import random
import numpy as np
from fractions import Fraction
import time
import re

def is_true(a):

    a = str(a)
    if len(a)>1:
        return a == get_huiwei(a)
    else:
        return True


def get_huiwei(a):
    return ''.join([a[len(a) - i - 1] for i in range(len(a))])



def huiwen_number(num):
    start = time.time()
    print('input:',num)
    lens = len(str(num))
    print('lens:',lens)
    # print(num/lens)
    # s=100000 if num/lens>1 else 2 if num/lens==1 else num
    num1=num-1
    num2=num+1
    count=0


    if lens>=10:
        lens1 = len(str(num1))
        head1 = str(int(str(num1)[:lens1/2])-1)
        head2 = str(int(head1) + 1)
        head3 = str(int(head2) + 1)
        if lens1 % 2:
            mid = str(num1)[lens1 / 2]
            num1 = int(head1 + mid + get_huiwei(head1))
            num2 = int(head2 + mid + get_huiwei(head2))
            num3 = int(head3 + mid + get_huiwei(head3))
        else:
            num1 = int(head1 + get_huiwei(head1))
            num2 = int(head2 + get_huiwei(head2))
            num3 = int(head3 + get_huiwei(head3))
        print(num1,num2,num3)
        delta_list=map(lambda x:abs(x-num),[num1,num2,num3])
        delta=min(delta_list)
        min_index = delta_list.index(delta)
        print(delta_list.index(delta))
        xx = num1 if min_index==0 else num2 if min_index==1 else num3
    else:
        while not is_true(num1) and not is_true(num2):
            num1-=1
            num2+=1
            count+=1
        if is_true(num1) and is_true(num2):
            xx = num1 if abs(num1 - num) <= abs(num2 - num) else num2
        else:
            xx = str(num1) if is_true(num1) else str(num2)
        print('count: ',count)

        print(num1,num2)

    end = time.time()
    print('new_number:',xx)
    print('runtime:',end-start)



def line_problems_solve(input_list):
    i=100
    count_l=[]
    # dot_list = [[random.randrange(n), random.randrange(n)] for _ in range(n)]
    # print(dot_list)
    while i>0:
        # random.shuffle(dot_list)
        node_list=random.sample(input_list,2)
        # print(node_list)
        x_list=map(lambda x:x[0],node_list)
        y_list = map(lambda x: x[1], node_list)
        # print('X:',x_list)
        # print('Y:', y_list)
        count = 2
        if x_list[1]-x_list[0]!=0:
            a=Fraction((y_list[1]-y_list[0]),(x_list[1]-x_list[0]))
            b = y_list[1] - a * x_list[1]
            # print(b)
            for s in input_list:
                if s not in node_list:
                    if a * s[0] + b ==s[1]:
                        count += 1
        else:
            for s in input_list:
                if s not in node_list:
                    if s[0]==x_list[1]:
                        count+=1

        if count>=2:
            count_l.append(count)
        i -= 1
    if count_l:
        print(max(count_l))


                # x_list*a+b=y_list



class Solution(object):
    def isRectangleOverlap(self, rec1, rec2):
        """
        :type rec1: List[int]
        :type rec2: List[int]
        :rtype: bool
        """
        p1=[[x,y] for x in list(np.linspace(rec1[0],rec1[2],1000)) for y in list(np.linspace(rec1[1],rec1[3],1000)) ]
        for z in p1:
            if z[0]>rec2[0] and z[0]<rec2[2]:
                if z[1]>rec2[1] and z[1]<rec2[3]:
                    return True
        return False


def canJump( nums):
    """
    :type nums: List[int]
    :rtype: bool
    """

    max_reach, last_index = 0, len(nums) - 1
    for i, x in enumerate(nums):
        print(i,x)
        if max_reach < i:
            return False
        if max_reach >= last_index:
            return True
        max_reach = max(max_reach, i + x)
        print('dssd',max_reach)

def jump(nums):
       n = len(nums)
       if(n <= 1):
           return False
       cur = nums[0]  #当前跳到的最远距离
       next = nums[0] #下一步能跳到的最远距离
       step = 1
       for i in range(1,n):
           if(cur < i):
               cur = next
               step+=1
           if(i + nums[i] > next):
               next = i + nums[i]
           if(cur >= n-1):
               return True
       return False

def atom_solve(formula):
    # s = re.findall(r'\((.*)\)',formula)
    # s = re.search(r'\((.*)\)',formula).group()
    lens = len(formula)
    for i in range(lens-1,-1,-1):
            if re.findall(r'\)', formula[i]):
                    print('i: ', i)
                    print('number: '+formula[i:].strip(')'))
                    print(formula[:i])
                    if re.findall(r'\(', formula[:i]):
                        print('')
                        atom_solve(formula[:i])
                    # print('j: ',j)
                    # print(formula[:j])
                    # break


        # if re.findall(r'\d',formula[x]):
        #     print(formula[x])
        #     print('index:',x)

def mid_num(nums1,nums2):
    num1 = sorted(nums1)
    nums2 = sorted(nums2)
    lens1 = len(nums1)
    lens2 = len(nums2)
    if lens1 <=1:
        mid1 = nums1[0] if nums1 else 0
    elif lens1 % 2:
        mid1 = nums1[lens1 / 2]
    else:
        mid1 = float(nums1[lens1 / 2] + nums1[lens1 / 2 - 1]) / 2

    if lens2 <= 1:
        mid2 = nums2[0] if nums2 else 0
    elif lens2 % 2:
        mid2 = nums2[lens2 / 2]
    else:
        mid2 = float(nums2[lens2 / 2] + nums2[lens2 / 2 - 1]) / 2
    print(mid1,mid2)
    return float(mid1 + mid2) / 2 if mid1*mid2!=0 else mid1 if mid1 else mid2

import sys
#手工设置递归调用深度
sys.setrecursionlimit(1000000)
def add_list(arr):
    if len(arr) == 0:
        return 0
    elif len(arr) == 1:
        return arr[0]
    else:
        return arr[-1] + add_list(arr[:-1])

def score_solve(a, b):
    lens = len(a) if len(a)>=len(b) else len(b)
    score=[0,0]
    for i in range(lens):
        if a[i]>b[i]:
            score[0]+=1
        elif a[i]<b[i]:
            score[1]+=1
    return score

def aVeryBigSum(ar):
    if len(ar)==0:
        return 0
    elif len(ar)==1:
        return ar[0]
    else:
        return ar[0]+aVeryBigSum(ar[1:])

def diagonalDifference(arr):
    lens = len(arr)
    a_total = 0
    b_total = 0
    if lens==1:
        return abs(arr[0][0])
    else:
        for i in range(lens):
            for j in range(lens):
                if i==j:
                   a_total+=arr[i][j]
                if i+j==lens-1:
                    b_total+=arr[i][j]
        print(a_total,b_total)
        return abs(a_total-b_total)
def plusMinus(arr):
    x=y=z=0
    lens = len(arr)
    for s in arr:
        if s>0:
            x+=1
        elif s==0:
            y+=1
        else:
            z+=1
    return [float(x)/lens , float(z)/lens, float(y)/lens]
def staircase(n):
    for i in range(1,n+1):
        print((n-i)*' '+'#'*i)
def miniMaxSum(arr):
    arr1=arr
    print(arr,arr1)
    min_s = min(arr)
    max_s = max(arr1)
    min_index=arr.index(min_s)
    max_index=arr1.index(max_s)
    return sum([arr1[i] for i in range(len(arr)) if i!=max_index]),sum([arr[i] for i in range(len(arr)) if i!=min_index])


def formingMagicSquare(s):
    error_i_list = []
    for x in s:
        if sum(x)!=15:
            error_i_list.append(s.index(x))

    print(error_i_list)
    error_j_list=[]
    for i in range(len(s)):
        if sum(map(lambda x:x[i],s))!=15:
            error_j_list.append(i)
    print(error_j_list)
    error_list={}
    for i in error_i_list:
        for j in error_j_list:
            # if s[0][0]+s[2][2]==10 or s[0][2]+s[2][0]==10:
            print([i,j])
            if i!=j!=1:
                print('error_value:',s[i][j])
                error_list['%s,%s'%(i,j)]=s[i][j]
    print(error_list)
    # a=[]
    # for i in range(len(s)):
    #     for j in range(len(s)):
    #         a.append(s[i][j])
    # b=set(a)
    # lose_x = [i for i in range(1,10) if i not in b][0]
    # duplicate_x= list(set([x for x in a if a.count(x)>1]))[0]
    # print(duplicate_x)
    # print(lose_x)
    # return abs(lose_x-duplicate_x)
import random

#获取3*3magic square
def get_magix_m():

    magic_m=[]
    for _ in range(500000):
        x=range(1,10)
        random.shuffle(x)
        if len(set(x))==9 and x[4]==5:
            x_trans = [x[:3],x[3:-3],x[-3:]]
            i=0
            for y in x_trans:
                if sum(y)==15:
                    i+=1
            if i==3:
                if x_trans[0][0]+x_trans[2][2]==x_trans[0][2]+x_trans[2][0]==10:
                    j=0
                    for i in range(3):
                        if sum(list(map(lambda x:x[i],x_trans)))==15:
                            j+=1
                    if j==3:
                        if x_trans not in magic_m:
                            magic_m.append(x_trans)
    for x in magic_m:
        print(x)
    print(len(magic_m))
    # return magic_m

#九宫格 Sudoku
def get_Sudoku(n=3):
    for _ in range(10000):
        res_x=[]
        for _ in range(n*n):
            x=range(1,10)
            random.shuffle(x)
            if len(set(x))==9:
                x_trans = [x[:3], x[3:-3], x[-3:]]
                res_x.append(x_trans)
        if n==3:
            random.shuffle(res_x)
            split_x = [res_x[:n], res_x[n:-n], res_x[-n:]]
            random.shuffle(split_x)
            k=0
            for x in split_x:
                for i in range(3):
                    row_line=[]
                    for j in range(3):
                        row_line.extend(x[j][i])
                    # print(split_x)
                    # print(row_line)
                    if len(set(row_line))==9:
                        k+=1
            if k==n**2:
                print('real: ',split_x)




def check_magic(s):
    x=[]
    for i in range(3):
        for j in range(3):
            x.append(s[i][j])

    if len(set(x)) == 9 and x[4] == 5:
        x_trans = [x[:3], x[3:-3], x[-3:]]
        i = 0
        for y in x_trans:
            if sum(y) == 15:
                i += 1
        if i == 3:
            if x_trans[0][0] + x_trans[2][2] == x_trans[0][2] + x_trans[2][0] == 10:
                j = 0
                for i in range(3):
                    if sum(list(map(lambda x: x[i], x_trans))) == 15:
                        j += 1
                if j == 3:
                    return True
    return False

if __name__ == '__main__':
    # for i in range(2,21):
    #     print('n = '+str(i))
    # node_list =[[1,1],[2,2],[3,3]]
    # line_problems_solve(node_list)
    #2147483647 "835868090839964076"
    # huiwen_number(2129614212)
    # s=Solution()
    # print(s.isRectangleOverlap([0,0,1,1],[2,2,3,3]))
    # print(canJump([3,2,4]))
    # nums=[2,3,1,1,0,4]
    # print(jump(nums))
    # formula='K2(SO4)(OH)2'
    # atom_solve(formula)
    # print(mid_num([1,1],[1,2]))
    # s=[i for i in range(1000)]
    # print(add_list(s))
    # print(score_solve([5,6,7],[3,6,10]))
    # s = []
    # print(aVeryBigSum(s))
    # print(diagonalDifference([[11]]))
    # print(plusMinus([0,0,-1,1,1]))
    # staircase(1)
    # print(miniMaxSum([1,2,3,4,5]))
    # s=[[4,9,2],[3,5,7],[8,1,5]]
    # s_1=[[4,8,2],[4,5,7],[6,1,6]]
    # magic_s=[[8,3,4],[1,5,9],[6,7,2]]
    # print(formingMagicSquare(s_1))
    # get_magix_m()
    # print(check_magic(magic_s))
    get_Sudoku()