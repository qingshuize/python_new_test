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
    """

    :param nums: 台阶总数
    :return: 是否能成功

    """
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
    """

    :param formula:
    :return:
    """
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
    """

    :param nums1:
    :param nums2:
    :return:
    """
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
    """

    :param a:
    :param b:
    :return:
    """
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
    """

    :param arr:
    :return:
    """

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
    """

    :param arr:
    :return:
    """
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
    """

    :param arr:
    :return:
    """
    arr1=arr
    print(arr,arr1)
    min_s = min(arr)
    max_s = max(arr1)
    min_index=arr.index(min_s)
    max_index=arr1.index(max_s)
    return sum([arr1[i] for i in range(len(arr)) if i!=max_index]),sum([arr[i] for i in range(len(arr)) if i!=min_index])


def formingMagicSquare(s):
    """

    :param s:
    :return:
    """
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
    """

    :return:
    """
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
    """

    :param n:
    :return:
    """
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
    """

    :param s:
    :return:
    """
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

#动态规划
"""
给定一个数字三角形，找到从顶部到底部的最小路径和。每一步可以移动到下面一行的相邻数字上

"""



def minimumTotal(triangle):
    """

    :param triangle:输入三角形数组
    :return:返回最小路径和
    """
    s_t=time.time()
    lens = len(triangle)

    # 方法一
    res = [triangle[0]]
    N = len(triangle)
    for i in range(1, len(triangle)):
        res.append([])
        for j in range(len(triangle[i])):
            if j - 1 >= 0 and j < len(triangle[i - 1]):
                res[i].append(min(res[i - 1][j - 1], res[i - 1][j]) + triangle[i][j])
            elif j - 1 >= 0:
                res[i].append(res[i - 1][j - 1] + triangle[i][j])
            else:
                res[i].append(res[i - 1][j] + triangle[i][j])

    minvalue = min(res[N - 1])
    print(time.time()-s_t)
    return minvalue

    # 方法二
    # s = triangle[0][0]
    # j = 0
    # for i in range(1, lens):
    #     min_s = min(triangle[i][j], triangle[i][j + 1])
    #     j = j if min_s == triangle[i][j] else j + 1
    #     s += min_s
    # print(time.time() - s_t)
    # return s

    #方法三
    # for i in range(lens-2,-1,-1):
    #     for j in range(len(triangle[i])):
    #         triangle[i][j] += min(triangle[i + 1][j], triangle[i + 1][j + 1])
    # print(time.time() - s_t)
    # return triangle[0][0]


"""
给定一个只含非负整数的m*n网格，找到一条从左上角到右下角的可以使数字和最小的路径。
m*n 矩阵
"""
def minPathSum(grid):

    #方法一
    s=np.array(grid)
    m,n=s.shape
    print(m,n)
    for i in range(m):
        for j in range(n):
            if j==0 and i>0:
                s[i][j] += s[i-1][j]
            if i==0 and j>0:
                s[i][j] += s[i][j - 1]
            elif i>0 and j>0:
                s[i][j]+=min(s[i-1][j],s[i][j-1])
    return s[m-1][n-1]



"""
假设你正在爬楼梯，需要n步你才能到达顶部。但每次你只能爬一步或者两步，你能有多少种不同的方法爬到楼顶部？

"""
def climbStairs(n):

    """
    :param n: 总台阶数
    :return:总方法数
    """

    # 方法一：递归(耗时较长)
    # s=[0 for i in range(n)]
    # if n<=0:
    #     return 0
    # if n==1 or n==2:
    #     return n
    # return climbStairs(n-1)+climbStairs(n-2)

    #方法二
    # X = [1, 2]  # 分为1步和2步
    # cache = [0 for _ in range(n + 1)]
    # cache[0] = 0
    # for i in range(n + 1):
    #     cache[i] += sum(cache[i - x] for x in X if i - x > 0)
    #     cache[i] += 1 if i in X else 0
    # print(cache)
    # return cache[-1]

    #方法三
    if n == 0:
        return 1
    if n <= 2:
        return n
    result = [1, 2]
    for i in range(n - 2):
        result.append(result[-2] + result[-1])
    print(result)
    return result[-1]

def c( m, n):
    mp = {}
    for i in range(m):
        for j in range(n):
            if (i == 0 or j == 0):
                mp[(i, j)] = 1
            else:
                mp[(i, j)] = mp[(i - 1, j)] + mp[(i, j - 1)]
    return mp[(m - 1, n - 1)]


"""
有一个机器人的位于一个 m × n 个网格左上角。

机器人每一时刻只能向下或者向右移动一步。机器人试图达到网格的右下角。

问有多少条不同的路径？

"""
def uniquePaths(m, n):

    print(m, n)
    s={}
    for i in range(m):
        for j in range(n):
            if (i == 0 or j == 0):
                s[(i, j)] = 1
            else:
                s[(i, j)] = s[(i - 1, j)] + s[(i, j - 1)]
    return s[(m-1,n-1)]


"""
"不同的路径" 的跟进问题：

现在考虑网格中有障碍物，那样将会有多少条不同的路径？

网格中的障碍和空位置分别用 1 和 0 来表示
"""
def uniquePathsWithObstacles(ob):
    s=ob
    for i in range(len(s)):
        for j in range(len(s[i])):
            if i == 0 and j == 0:
                s[i][j] = 1-s[i][j]
            elif i==0:
                if s[i][j]==1:
                    s[i][j]=0
                else:
                    s[i][j]=s[i][j-1]
            elif j==0:
                if s[i][j]==1:
                    s[i][j]=0
                else:
                    s[i][j]=s[i-1][j]
            else:
                if s[i][j]==1:
                    s[i][j]=0
                else:
                    s[i][j] = s[i-1][j] + s[i][j-1]
    print(s)
    if s[-1][-1] > 2147483647:
        return -1
    else:
        return s[-1][-1]


"""
给定一个整数数组（下标从 0 到 n-1， n 表示整个数组的规模），
请找出该数组中的最长上升连续子序列。
（最长上升连续子序列可以定义为从右到左或从左到右的序列。）
"""

def longestIncreasingContinuousSubsequence(A):


    #方法一
    lens=len(A)
    if lens<=1:
        return lens
    if A is None:
        return 0

    maxnum=1
    cur = 1

    INC = 0
    DEC = 1
    EQL = 2
    STATUS = EQL

    for i in range(1,lens):
        if A[i]>A[i-1]:
            if STATUS==DEC:
                cur=2
            else:
                cur+=1
                maxnum=max(maxnum,cur)
            STATUS=INC
        elif A[i]<A[i-1]:
            if STATUS==INC:
                cur=2
            else:
                cur+=1
                maxnum=max(maxnum,cur)
            STATUS=DEC
        else:
            STATUS=EQL
            cur=1
    return maxnum

    #方法二
    # if not A:
    #     return 0
    #
    # cur = cur1 = 1
    # mx = mx1 = 1
    #
    # for i in range(1, len(A)):
    #     if A[i] > A[i - 1]:
    #         cur += 1
    #         mx = max(mx, cur)
    #     else:
    #         cur = 1
    # print('从左向右：'+str(mx))
    #
    # for i in range(len(A) - 2, -1, -1):
    #     if A[i] > A[i + 1]:
    #         cur1 += 1
    #         mx1 = max(mx1, cur1)
    #     else:
    #         cur1 = 1
    # print('从右向左：'+str(mx1))
    #
    # return mx if mx>mx1 else mx1


"""
我们有一个栅栏，它有n个柱子，现在要给柱子染色，有k种颜色可以染。
必须保证不存在超过2个相邻的柱子颜色相同，求有多少种染色方案
"""
def numWays(n, k):
    x = [0, k, k * k]
    if n <= 2:
        return x[n]
    if k == 1 and n >= 3:
        return 0
    for i in range(2, n):
        x.append((k - 1) * (x[-1] + x[-2]))

    return x[-1]


class NumArray(object):
    """
    Given an integer array nums, find the sum of the elements between indices i and j (i ≤ j), inclusive.
    """
    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        if len(nums) == 0:
            return

        n = len(nums)

        self.dp = [0 for _ in range(n+1)]
        for r in range(n):
            self.dp[r] = self.dp[r] + nums[r]+self.dp[r-1]

    def sumRange(self, i, j):
        """
        :type i: int
        :type j: int
        :rtype: int
        """
        # print(nums[i:j+1])
        # return sum(nums[i:j+1])
        # return self.dp
        return self.dp[j] - self.dp[i]+(self.dp[i]-self.dp[i-1])


"""
约翰想在他家后面的空地上建一个后花园，现在有两种砖，
一种3 dm的高度，7 dm的高度。约翰想围成x dm的墙。
如果约翰能做到，输出YES，否则输出NO。
"""
def isBuild(x):
    #a*x+b*y=z


    #方法一
    i = x / 7
    while i >= 0:
        if not (x - 7 * i) % 3:
            return 'YES'
        i -= 1
    return 'NO'

    #方法二
    # dp = [0 for i in range(1001)]
    # dp[0] = 1
    # for i in range(3, x + 1):
    #     if dp[i - 3] == 1:
    #         dp[i] = 1
    # for i in range(7, x + 1):
    #     if dp[i - 7] == 1:
    #         dp[i] = 1
    # print(dp)
    # if dp[x] == 1:
    #     return "YES"
    # else:
    #     return "NO"

import copy

def twoSum(nums, target):

    #方法一
    # hash用于建立数值到下标的映射
    hash = {}
    # 循环nums数值，并添加映射
    for i in range(len(nums)):
        if target - nums[i] in hash:
            return [hash[target - nums[i]], i]
        hash[nums[i]] = i
    # 无解的情况
    return [-1, -1]

    #方法二
    # for i, a in enumerate(numbers):
    #     for j, b in enumerate(numbers[i + 1 - len(numbers):]):
    #         if a + b == target:
    #             return [i, j + i + 1]
    # return [-1, -1]

    # s=[0 for i in range(len(numbers))]
    # for i in range(len(numbers)):
    #     x=copy.copy(numbers)
    #     x.remove(numbers[i])
    #     if target-numbers[i] in x:
    #         s[i]+=1
    # print(s)
    # return [i for i in range(len(s)) if s[i]==1]

"""

给出三个字符串:s1、s2、s3，判断s3是否由s1和s2交叉构成。
"""
def isInterleave(s1, s2, s3):
    if not s1 or not s2 or not s3:
        return False
    if len(s1)+len(s2)!=len(s3):
        return False
    x1=dict(enumerate(s1))
    x2 = dict(enumerate(s2))
    x3=dict(enumerate(s3))
    print(x1,x2)


    # interleave = [[False] * (len(s2) + 1) for i in range(len(s1) + 1)]
    # print(interleave)
    # interleave[0][0] = True
    # for i in range(len(s1)):
    #     interleave[i + 1][0] = s1[:i + 1] == s3[:i + 1]
    # for i in range(len(s2)):
    #     interleave[0][i + 1] = s2[:i + 1] == s3[:i + 1]
    # print(interleave)
    #
    # for i in range(len(s1)):
    #     for j in range(len(s2)):
    #         interleave[i + 1][j + 1] = False
    #         if s1[i] == s3[i + j + 1]:
    #             interleave[i + 1][j + 1] = interleave[i][j + 1]
    #         if s2[j] == s3[i + j + 1]:
    #             interleave[i + 1][j + 1] |= interleave[i + 1][j]
    # return interleave[len(s1)][len(s2)]


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
    # get_Sudoku()
    s=[[-1],[2,3],[0,3,2],[1,-1,-3,2],[0,4,-2,-2,3],[2,2,-3,-1,0,2]]
    # print(minimumTotal(s))
    s1=[[1,2],[1,1],[3,0]]
    # print(minPathSum(s1))
    # print(climbStairs(39))
    # print(uniquePaths(12,3))
    ob=[
        [0,0],
        [0,0],
        [0,0],
        [1,0],
        [0,0]]
    # ob=[[0,0,0],[1,0,0],[0,0,0],[1,1,0]]
    # print(uniquePathsWithObstacles(ob))
    D=[1,3,0,-2,3,4,2,1,6,8,20,9,0,-1]
    # print(longestIncreasingContinuousSubsequence([5,4,2,1,3]))
    # print(numWays(3,2))
    # s=NumArray([-2, 0, 3, -5, 2, -1])
    # print(s.sumRange(0,5))
    # print(isBuild(101))
    # print(twoSum([2, 7, 11, 15],9))
    print(isInterleave('dad','frfef','dfarfefd'))