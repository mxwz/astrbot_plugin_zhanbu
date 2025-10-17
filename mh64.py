import time
import random
import math
from datetime import datetime
from zhdate import ZhDate
from typing import Iterable, Callable, Union
import re
from gua_64 import *

# !/usr/local/sbin/python3
# -*- coding:utf-8 -*-


dict1 = {}

# 数字提取
with open('htmlnum.txt', 'r') as f:
    lines = f.readlines()  # 逐行读取文件内容，保存为一个列表

nums = []  # 初始化一个空列表，用于存放提取出的数字
for line in lines:
    line = line.strip()  # 去除每行的空白和换行符
    if line.isdigit():  # 判断当前行是否为数字
        nums.append(int(line))  # 将当前行的数字转为整数，并添加到列表中

# 文字提取
with open('cash.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()  # 逐行读取文件内容，保存为一个列表

lst = []  # 初始化一个空列表，用于存储转换后的字符串
for line in lines:
    s = line.strip()  # 去除每行的空白字符和换行符
    if s:  # 判断处理后的内容是否为空或空白字符
        lst.append(s)  # 将非空的内容添加到列表中

# 卦象对应的文件名装入字典
for i in range(64):
    dict1[lst[i]] = nums[i]

# def Seach_txt(x):
#     with open('./64/%d.txt' % (dict1[x]), 'r', encoding='utf-8') as file:
#         content = ''
#         start = False  # 标志是否匹配到了"传统解卦"
#         for line in file:
#             if re.search(r'传统解卦', line):
#                 start = True  # 匹配到关键字后开始保存
#             if start:
#                 content += line  # 拼接累计读取的行
#             if re.search(r'决策', line):
#                 break  # 匹配到第二个关键字，跳出循环
#     print(content)


tiangan = ['甲', '⼄', '丙', '丁', '戊', '⼰', '庚', '⾟', '壬', '癸']
dizhi = ['⼦', '丑', '寅', '卯', '⾠', '巳', '午', '未', '申', '⾣', '戌', '亥']
index = 0
s = 1
list1 = []
list2 = []
list3 = []
list5 = []
list6 = []
list7 = []
l = []
while index < 60:
    l.append(tiangan[index % 10] + dizhi[index % 12])
    index = index + 1

chinese_char_map = {}
with open('./chinese_unicode_table.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for line in lines[6:]:  # 前6行是表头，去掉
        line_info = line.strip().split()
        # 处理后的数组第一个是文字，第7个是笔画数量
        chinese_char_map[line_info[0]] = line_info[6]


def __sort_by_strokes_core(words: Iterable) -> int:
    """
    统计字符串中所有文字的笔画总数

    :param words: 需要统计的字符串
    :return: 笔画总数
    """
    strokes = 0
    for word in words:
        if 0 <= ord(word) <= 126:  # 数字，英文符号范围
            strokes += 1
        elif 0x4E00 <= ord(word) <= 0x9FA5:  # 常用汉字Unicode编码范围4E00-9FA5，20902个字
            strokes += int(chinese_char_map.get(word, 1))
        else:  # 特殊符号字符一律排在最后
            strokes += 1
    return strokes


# 八卦属性
def BG_sx(x):
    if x == '乾' or x == '兑':
        return '金'
    elif x == '离':
        return '火'
    elif x == '震' or x == '巽':
        return '木'
    elif x == '坎':
        return '水'
    else:
        return '土'


# 八卦类属
def BG_ls(x):
    if x == '乾':
        return '天'
    elif x == '兑':
        return '泽'
    elif x == '离':
        return '火'
    elif x == '震':
        return '雷'
    elif x == '巽':
        return '风'
    elif x == '坎':
        return '水'
    elif x == '坤':
        return '地'
    else:
        return '山'


# 定义地支函数
def dizhi(shichen):
    if 1 <= shichen < 3:
        return '丑'
    elif 3 <= shichen < 5:
        return '寅'
    elif 5 <= shichen < 7:
        return '卯'
    elif 7 <= shichen < 9:
        return '辰'
    elif 9 <= shichen < 11:
        return '巳'
    elif 11 <= shichen < 13:
        return '午'
    elif 13 <= shichen < 15:
        return '未'
    elif 15 <= shichen < 17:
        return '申'
    elif 17 <= shichen < 19:
        return '酉'
    elif 19 <= shichen < 21:
        return '戌'
    elif 21 <= shichen < 23:
        return '亥'
    else:
        return '子'


# 起卦先天数
def xiantian(x):
    if x % 8 == 1:
        return '乾'
    elif x % 8 == 2:
        return '兑'
    elif x % 8 == 3:
        return '离'
    elif x % 8 == 4:
        return '震'
    elif x % 8 == 5:
        return '巽'
    elif x % 8 == 6:
        return '坎'
    elif x % 8 == 7:
        return '艮'
    else:
        return '坤'


def wx_num(x):
    if x == '水':
        return 1
    elif x == '木':
        return 2
    elif x == '火':
        return 3
    elif x == '土':
        return 4
    else:  # 金
        return 5


def SK(t, y):
    if int(math.fabs(t)) - int(math.fabs(y)) == 1:
        return 1
    elif int(math.fabs(t)) - int(math.fabs(y)) == -1:
        return -1
    elif int(math.fabs(t)) - int(math.fabs(y)) == 2:
        return 2
    elif int(math.fabs(t)) - int(math.fabs(y)) == -2:
        return -2
    elif int(math.fabs(t)) - int(math.fabs(y)) == 3:
        return 3
    elif int(math.fabs(t)) - int(math.fabs(y)) == -3:
        return -3
    elif int(math.fabs(t)) - int(math.fabs(y)) == 4:
        return 4
    elif int(math.fabs(t)) - int(math.fabs(y)) == -4:
        return -4
    else:
        if BG_up == BG_down:
            return 5
        else:
            return 6


# 0为比和，1为生我，-1为我生，2为克我，-2为我克，3为克我，-3为我克，4为我克，-4为克我，5为比劫，6为比助


def TY_pd(n):
    if x == 1:
        t = BG_down
        y = BG_up
        if n == 't':
            return t
        else:
            return y

    else:
        t = BG_up
        y = BG_down
        if n == 't':
            return t
        else:
            return y


# x为上，y为下
def G64(x, y):
    # 乾卦
    if x == '乾' and y == '乾':
        return '乾为天'
    elif x == '乾' and y == '兑':
        return '天泽履'
    elif x == '乾' and y == '离':
        return '天火同人'
    elif x == '乾' and y == '震':
        return '天雷无妄'
    elif x == '乾' and y == '巽':
        return '天风姤'
    elif x == '乾' and y == '坎':
        return '天水讼'
    elif x == '乾' and y == '艮':
        return '天山遁'
    elif x == '乾' and y == '坤':
        return '天地否'

    # 兑卦
    elif x == '兑' and y == '乾':
        return '泽天夬'
    elif x == '兑' and y == '兑':
        return '兑为泽'
    elif x == '兑' and y == '离':
        return '泽火革'
    elif x == '兑' and y == '震':
        return '泽雷随'
    elif x == '兑' and y == '巽':
        return '泽风大过'
    elif x == '兑' and y == '坎':
        return '泽水困'
    elif x == '兑' and y == '艮':
        return '泽山咸'
    elif x == '兑' and y == '坤':
        return '泽地萃'

    # 离卦
    elif x == '离' and y == '乾':
        return '火天大有'
    elif x == '离' and y == '兑':
        return '火泽睽'
    elif x == '离' and y == '离':
        return '离为火'
    elif x == '离' and y == '震':
        return '火雷噬嗑'
    elif x == '离' and y == '巽':
        return '火风鼎'
    elif x == '离' and y == '坎':
        return '火水未济'
    elif x == '离' and y == '艮':
        return '火山旅'
    elif x == '离' and y == '坤':
        return '火地晋'

    # 震卦
    elif x == '震' and y == '乾':
        return '雷天大壮'
    elif x == '震' and y == '兑':
        return '雷泽归妹'
    elif x == '震' and y == '离':
        return '雷火丰'
    elif x == '震' and y == '震':
        return '震为雷'
    elif x == '震' and y == '巽':
        return '雷风恒'
    elif x == '震' and y == '坎':
        return '雷水解'
    elif x == '震' and y == '艮':
        return '雷山小过'
    elif x == '震' and y == '坤':
        return '雷地豫'

    # 巽卦
    elif x == '巽' and y == '乾':
        return '风天小畜'
    elif x == '巽' and y == '兑':
        return '风泽中孚'
    elif x == '巽' and y == '离':
        return '风火家人'
    elif x == '巽' and y == '震':
        return '风雷益'
    elif x == '巽' and y == '巽':
        return '巽为风'
    elif x == '巽' and y == '坎':
        return '风水涣'
    elif x == '巽' and y == '艮':
        return '风山渐'
    elif x == '巽' and y == '坤':
        return '风地观'

    # 坎卦
    elif x == '坎' and y == '乾':
        return '水天需'
    elif x == '坎' and y == '兑':
        return '水泽节'
    elif x == '坎' and y == '离':
        return '水火既济'
    elif x == '坎' and y == '震':
        return '水雷屯'
    elif x == '坎' and y == '巽':
        return '水风井'
    elif x == '坎' and y == '坎':
        return '坎为水'
    elif x == '坎' and y == '艮':
        return '水山蹇'
    elif x == '坎' and y == '坤':
        return '水地比'

    # 艮卦
    elif x == '艮' and y == '乾':
        return '山天大畜'
    elif x == '艮' and y == '兑':
        return '山泽损'
    elif x == '艮' and y == '离':
        return '山火贲'
    elif x == '艮' and y == '震':
        return '山雷颐'
    elif x == '艮' and y == '巽':
        return '山风蛊'
    elif x == '艮' and y == '坎':
        return '山水蒙'
    elif x == '艮' and y == '艮':
        return '艮为山'
    elif x == '艮' and y == '坤':
        return '山地剥'

    # 坤卦
    elif x == '坤' and y == '乾':
        return '地天泰'
    elif x == '坤' and y == '兑':
        return '地泽临'
    elif x == '坤' and y == '离':
        return '地火明夷'
    elif x == '坤' and y == '震':
        return '地雷复'
    elif x == '坤' and y == '巽':
        return '地风升'
    elif x == '坤' and y == '坎':
        return '地水师'
    elif x == '坤' and y == '艮':
        return '地山谦'
    else:
        return '坤为地'


def BG_line(x):
    if x == '乾':
        return '\t——————\n\t——————\n\t——————'
    elif x == '兑':
        return '\t——  ——\n\t——————\n\t——————'
    elif x == '离':
        return '\t——————\n\t——  ——\n\t——————'
    elif x == '震':
        return '\t——  ——\n\t——  ——\n\t——————'
    elif x == '巽':
        return '\t——————\n\t——————\n\t——  ——'
    elif x == '坎':
        return '\t——  ——\n\t——————\n\t——  ——'
    elif x == '坤':
        return '\t——  ——\n\t——  ——\n\t——  ——'
    else:
        return '\t——————\n\t——  ——\n\t——  ——'


def yao(x):
    if x == '阴':
        return '——  ——'
    else:
        return '——————'


def yao_2(x):
    if x == '——  ——':
        return '阴'
    else:
        return '阳'


def yao_3(x, y, z):
    if x == '——————' and y == '——————' and z == '——————':
        return '乾'
    elif x == '——  ——' and y == '——————' and z == '——————':
        return '兑'
    elif x == '——————' and y == '——  ——' and z == '——————':
        return '离'
    elif x == '——  ——' and y == '——  ——' and z == '——————':
        return '震'
    elif x == '——————' and y == '——————' and z == '——  ——':
        return '巽'
    elif x == '——  ——' and y == '——————' and z == '——  ——':
        return '坎'
    elif x == '——————' and y == '——  ——' and z == '——  ——':
        return '艮'
    else:
        return '坤'


def yao_4(x):
    if x == '乾':
        y_1 = '阳'
        y_2 = '阳'
        y_3 = '阳'
        list3.append(y_1)
        list3.append(y_2)
        list3.append(y_3)
        return list3
    elif x == '兑':
        y_1 = '阴'
        y_2 = '阳'
        y_3 = '阳'
        list3.append(y_1)
        list3.append(y_2)
        list3.append(y_3)
        return list3
    elif x == '离':
        y_1 = '阳'
        y_2 = '阴'
        y_3 = '阳'
        list3.append(y_1)
        list3.append(y_2)
        list3.append(y_3)
        return list3
    elif x == '震':
        y_1 = '阴'
        y_2 = '阴'
        y_3 = '阳'
        list3.append(y_1)
        list3.append(y_2)
        list3.append(y_3)
        return list3
    elif x == '巽':
        y_1 = '阳'
        y_2 = '阳'
        y_3 = '阴'
        list3.append(y_1)
        list3.append(y_2)
        list3.append(y_3)
        return list3
    elif x == '坎':
        y_1 = '阴'
        y_2 = '阳'
        y_3 = '阴'
        list3.append(y_1)
        list3.append(y_2)
        list3.append(y_3)
        return list3
    elif x == '坤':
        y_1 = '阴'
        y_2 = '阴'
        y_3 = '阴'
        list3.append(y_1)
        list3.append(y_2)
        list3.append(y_3)
        return list3
    else:
        y_1 = '阳'
        y_2 = '阴'
        y_3 = '阴'
        list3.append(y_1)
        list3.append(y_2)
        list3.append(y_3)
        return list3


def yao_fan(x):
    if x == '阴':
        return '阳'
    else:
        return '阴'


def yao_fan_yy(x):
    if x == '——  ——':
        return '——————'
    else:
        return '——  ——'


# 新历农历转换
create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# 新历年月日
year = int(create_time[0:4])
mouth = int(create_time[5:7])
day = int(create_time[8:10])
hourtime = int(create_time[11:13])
mintime = int(create_time[14:16])
# 新建新历
xin = datetime(year, mouth, day)
# 转换农历
nong = str(ZhDate.from_datetime(xin))
# 农历年月日
n_year = int(nong[2:6])
'''
n_mouth = int(nong[7:9])
n_day = int(nong[10:12])
'''
if nong[7].isdigit():  # 排除闰二月
    if nong[8].isdigit():  # 两位数月份
        n_mouth = int(nong[7:9])
        # 日期：天
        if nong[11].isdigit():  # 二位数日期
            n_day = int(nong[10:12])
        else:  # 个位数日期
            n_day = int(nong[10])

    else:  # 一位数月份
        n_mouth = int(nong[7])
        # 日期：天
        if nong[10].isdigit():  # 二位数日期
            n_day = int(nong[9:11])
        else:  # 个位数日期
            n_day = int(nong[9])

else:  # 闰二月
    n_mouth = int(nong[8])
    # 日期：天
    if nong[11].isdigit():  # 二位数日期
        n_day = int(nong[10:12])
    else:  # 个位数日期
        n_day = int(nong[10])
# 获取新历时辰
hour = int(time.strftime('%H', time.localtime(time.time())))
# 地支
time_dz = dizhi(hour)


# 地支序号
def sc_num():
    if time_dz == '子':
        return 1
    elif time_dz == '丑':
        return 2
    elif time_dz == '寅':
        return 3
    elif time_dz == '卯':
        return 4
    elif time_dz == '辰':
        return 5
    elif time_dz == '巳':
        return 6
    elif time_dz == '午':
        return 7
    elif time_dz == '未':
        return 8
    elif time_dz == '申':
        return 9
    elif time_dz == '酉':
        return 10
    elif time_dz == '戌':
        return 11
    else:
        return 12

    # 获取地支序号
def Main():
    global BG_down
    global BG_up
    global time_dz
    q = input('请输入你的问题：')
    p = input('请输入性别：')
    a = int(input('''\n请选择起数方式：
    1.时间起数；
    2.笔画起数（仅支持两字到六字）；
    3.随机数字起数；
    4.自定义数字起数;
    5.三数起数（第一个数字为上卦，第二个数字为下卦，第三个数字为动爻）:\n
    '''))

    try:
        d = int(input('\n请问是否需要更改时辰数据？是请按1，不是请随意输入其他数字后回车：'))
    except ValueError:
        d = 0
    if d == 1:
        n = input('请输入时辰名，例如“子”：')
        time_dz = n

    n_year_num = (n_year % 60) - 3
    n_ymd = n_year_num + n_mouth + n_day
    n_ymdh = n_ymd + sc_num()


    def main():
        global num_yao
        global s
        global x
        global num_up
        global num_down
        while True:
            if a == 1:
                num_up = n_ymd
                num_down = n_ymdh
                num_yao = n_ymdh % 6
                if num_yao == 0:
                    num_yao = 6
                break

            elif a == 2:
                b = int(input('请问需要输入几个汉字？（2-6）：'))
                while s <= b:
                    z = input('请输入第%s个字:' % s)
                    if len(z) == 1:
                        if u'\u4e00' <= z <= u'\u9fa5':
                            list1.append(z)
                            s += 1
                        else:
                            print('\n非法输入，请重新输入\n')
                            continue
                    else:
                        print('\n只能输入一个字，请重新输入\n')
                        continue
                print('您输入的汉字为', list1)
                for i in list1:
                    n = __sort_by_strokes_core(i)
                    list2.append(n)

                num_up = 0
                num_down = 0
                num_yao = 0
                if len(list1) % 2 == 0:  # 判断偶数
                    for i in list2[:(len(list1) // 2)]:  # 偶数下，均衡分配
                        num_up += i
                    for k in list2[(len(list1) // 2):]:
                        num_down += k
                else:
                    for i in list2[:(len(list1) // 2)]:  # 偶数下，均衡分配
                        num_up += i
                    for k in list2[(len(list1) // 2):]:
                        num_down += k

                num_yao = (num_up + num_down + sc_num()) % 6
                if num_yao == 0:
                    num_yao = 6
                break

            elif a == 3:
                b = int(input('请问需要输入几位数？（2-6）：'))
                while True:
                    if 2 <= b <= 6:
                        for i in range(b):
                            c = random.randint(1, 20)
                            list1.append(c)

                        print('随机抽取的数字为', list1)

                        num_up = 0
                        num_down = 0
                        num_yao = 0
                        if len(list1) % 2 == 0:  # 判断偶数
                            for i in list1[:(len(list1) // 2)]:  # 偶数下，均衡分配
                                num_up += i
                            for k in list1[(len(list1) // 2):]:
                                num_down += k

                        else:  # 判断为奇数
                            for i in list1[:(len(list1) // 2)]:  # 奇数前少后多相差1
                                num_up += i
                            for k in list1[(len(list1) // 2):]:
                                num_down += k

                        num_yao = (num_up + num_down + sc_num()) % 6
                        if num_yao == 0:
                            num_yao = 6
                        break
                    else:
                        print('非法输入，请重新输入！')
                        continue

                break

            elif a == 4:
                b = int(input('请问需要输入几位数？（2-6）：'))
                print('请随机输入%d个不为零的正整数：' % b)
                while s <= b:
                    num = int(input('请输入第%s个数字:' % s))
                    if num <= 0:
                        print('\n非法输入，请重新输入\n')
                        continue
                    list1.append(num)
                    s += 1
                print('您输入的数字为', list1)

                num_up = 0
                num_down = 0
                num_yao = 0  # 上少下多
                if len(list1) % 2 == 0:  # 判断偶数
                    for i in list1[:(len(list1) // 2)]:  # 偶数下，均衡分配
                        num_up += i
                    for k in list1[(len(list1) // 2):]:
                        num_down += k
                else:
                    for i in list1[:(len(list1) // 2)]:  # 偶数下，均衡分配
                        num_up += i
                    for k in list1[(len(list1) // 2):]:
                        num_down += k

                num_yao = (num_up + num_down + sc_num()) % 6
                if num_yao == 0:
                    num_yao = 6
                break

            elif a == 5:

                while True:
                    d = int(input('请选择：1.自行输入；2.随机抽取（1-20）'))
                    if d == 1:
                        print('请随机输入3个不为零的正整数：')
                        while s <= 3:
                            num = int(input('请输入第%s个数字:' % s))
                            if num > 0:
                                list1.append(num)
                                s += 1
                            else:
                                print('\n非法输入，请重新输入\n')
                                continue

                        print('您输入的数字为', list1)
                        num_up = list1[0]
                        num_down = list1[1]

                        while True:
                            g = int(input('请选择：1第三位数直接算出动爻.；2.第三位数+时辰序号算出动爻'))
                            if g == 1:
                                num_yao = list1[2] % 6
                                break
                            elif g == 2:
                                num_yao = (list1[2] + sc_num()) % 6
                                break
                            else:
                                print('\n非法输入，请重新输入\n')
                                continue
                        if num_yao == 0:
                            num_yao = 6
                        break

                    elif d == 2:
                        for i in range(3):
                            c = random.randint(1, 20)
                            list1.append(c)
                        print('随机抽取的数字为', list1)
                        num_up = list1[0]
                        num_down = list1[1]

                        while True:
                            g = int(input('请选择：1.第三位数直接算出动爻；2.第三位数+时辰序号算出动爻'))
                            if g == 1:
                                num_yao = list1[2] % 6
                                break
                            elif g == 2:
                                num_yao = (list1[2] + sc_num()) % 6
                                break
                            else:
                                print('\n非法输入，请重新输入\n')
                                continue
                        if num_yao == 0:
                            num_yao = 6
                        break

                    else:
                        print('\n非法输入，请重新输入\n')
                        continue

                break

            else:
                print('\n非法输入，请重新输入\n')
                continue

        if num_yao > 3:
            x = 1  # 下卦为体，上卦为用
        else:
            x = 0

    # 定义体用关系
    def TY():
        if SK(wx_num(BG_sx(TY_pd('t'))), wx_num(BG_sx(TY_pd('y')))) == 1:
            return '----用生体----'
        elif SK(wx_num(BG_sx(TY_pd('t'))), wx_num(BG_sx(TY_pd('y')))) == -1:
            return '----体生用----'
        elif SK(wx_num(BG_sx(TY_pd('t'))), wx_num(BG_sx(TY_pd('y')))) == 2:
            return '----用克体----'
        elif SK(wx_num(BG_sx(TY_pd('t'))), wx_num(BG_sx(TY_pd('y')))) == -2:
            return '----体克用----'
        elif SK(wx_num(BG_sx(TY_pd('t'))), wx_num(BG_sx(TY_pd('y')))) == 3:
            return '----体克用----'
        elif SK(wx_num(BG_sx(TY_pd('t'))), wx_num(BG_sx(TY_pd('y')))) == -3:
            return '----用克体----'
        elif SK(wx_num(BG_sx(TY_pd('t'))), wx_num(BG_sx(TY_pd('y')))) == 4:
            return '----体生用----'
        elif SK(wx_num(BG_sx(TY_pd('t'))), wx_num(BG_sx(TY_pd('y')))) == -4:
            return '----用生体----'
        elif SK(wx_num(BG_sx(TY_pd('t'))), wx_num(BG_sx(TY_pd('y')))) == 5:
            return '----体用比劫----'
        else:
            return '----体用比助----'



    main()


    BG_up = xiantian(num_up)
    BG_down = xiantian(num_down)

    # [0:6] 本卦总阴阳yy_1
    list4 = yao_4(BG_up) + yao_4(BG_down)
    yy_1 = list4[0:6]
    C_1 = list4[0:6]
    # 本卦阴阳转换图像
    for i in yy_1:
        m = yao(i)
        list5.append(m)
    # 本卦总图像
    yy_1_2 = list5
    C_2 = list5
    # 本卦的阴阳
    b_up_1 = yy_1[0:3]
    b_down_1 = yy_1[3:6]
    # 本卦的图像
    b_up_2 = yy_1_2[0:3]
    b_down_2 = yy_1_2[3:6]
    # 本卦上分解
    b_up_x = b_up_2[0]
    b_up_y = b_up_2[1]
    b_up_z = b_up_2[2]
    # 本卦下分解
    b_down_x = b_down_2[0]
    b_down_y = b_down_2[1]
    b_down_z = b_down_2[2]

    # 互卦的阴阳
    H_up_1 = yy_1[1:4]
    H_down_1 = yy_1[2:5]
    # 互卦的图像
    H_up_2 = yy_1_2[1:4]
    H_down_2 = yy_1_2[2:5]
    # 互卦上分解
    H_up_x = H_up_2[0]
    H_up_y = H_up_2[1]
    H_up_z = H_up_2[2]
    # 互卦下分解
    H_down_x = H_down_2[0]
    H_down_y = H_down_2[1]
    H_down_z = H_down_2[2]
    # 互卦组合
    H_up = yao_3(H_up_x, H_up_y, H_up_z)
    H_down = yao_3(H_down_x, H_down_y, H_down_z)

    # 变卦总阴阳yy_b
    yy_b = yy_1.copy()
    yy_b.reverse()
    m_1 = yy_b.pop(num_yao - 1)
    yy_b.insert(num_yao - 1, yao_fan(m_1))
    yy_b.reverse()
    # 变卦阴阳转图像
    for i in yy_b:
        m_3 = yao(i)
        list6.append(m_3)
    # 变卦总图像
    yy_b_2 = list6
    # 变卦的阴阳
    B_up_1 = yy_b[0:3]
    B_down_1 = yy_b[3:6]
    # 变卦的图像
    B_up_2 = yy_b_2[0:3]
    B_down_2 = yy_b_2[3:6]
    # 变卦上分解
    B_up_x = B_up_2[0]
    B_up_y = B_up_2[1]
    B_up_z = B_up_2[2]
    # 变卦下分解
    B_down_x = B_down_2[0]
    B_down_y = B_down_2[1]
    B_down_z = B_down_2[2]
    # 变卦组合
    B_up = yao_3(B_up_x, B_up_y, B_up_z)
    B_down = yao_3(B_down_x, B_down_y, B_down_z)

    # 综卦上分解
    Z_up_x = yao_fan_yy(b_up_x)
    Z_up_y = yao_fan_yy(b_up_y)
    Z_up_z = yao_fan_yy(b_up_z)
    # 综卦下分解
    Z_down_x = yao_fan_yy(b_down_x)
    Z_down_y = yao_fan_yy(b_down_y)
    Z_down_z = yao_fan_yy(b_down_z)
    # 综卦组合
    Z_up = yao_3(Z_up_x, Z_up_y, Z_up_z)
    Z_down = yao_3(Z_down_x, Z_down_y, Z_down_z)

    # 错卦总阴阳
    C_1.reverse()
    # 错卦总图像
    C_2.reverse()
    # 错卦的阴阳
    C_up_1 = C_1[0:3]
    C_down_1 = C_1[3:6]
    # 错卦的图像
    C_up_2 = C_2[0:3]
    C_down_2 = C_2[3:6]
    # 错卦上分解
    C_up_x = C_up_2[0]
    C_up_y = C_up_2[1]
    C_up_z = C_up_2[2]
    # 错卦下分解
    C_down_x = C_down_2[0]
    C_down_y = C_down_2[1]
    C_down_z = C_down_2[2]
    # 错卦组合
    C_up = yao_3(C_up_x, C_up_y, C_up_z)
    C_down = yao_3(C_down_x, C_down_y, C_down_z)

    time.sleep(1)
    print('—上卦:%s—\t—下卦:%s—\n\t———动爻为%s———' % (BG_up, BG_down, num_yao))
    print('上卦属性：%s\t下卦属性：%s' % (BG_sx(BG_up), BG_sx(BG_down)))
    print('上卦类属：%s\t下卦类属：%s\n' % (BG_ls(BG_up), BG_ls(BG_down)))

    print('\n体：%s\t用：%s' % (TY_pd('t'), TY_pd('y')))
    print(TY())
    print('\n')
    print('本卦：%s' % (G64(BG_up, BG_down)))
    print('%s\n%s\n' % (BG_line(BG_up), BG_line(BG_down)))
    print('互卦：%s' % (G64(H_up, H_down)))
    print('%s\n%s\n' % (BG_line(H_up), BG_line(H_down)))
    print('变卦：%s' % (G64(B_up, B_down)))
    print('%s\n%s\n' % (BG_line(B_up), BG_line(B_down)))
    print('综卦：%s' % (G64(Z_up, Z_down)))
    print('%s\n%s\n' % (BG_line(Z_up), BG_line(Z_down)))
    print('错卦：%s' % (G64(C_up, C_down)))
    print('%s\n%s\n' % (BG_line(C_up), BG_line(C_down)))

    while True:
        try:
            answer = int(input('请问需要查询卦象的信息吗？\n1、本卦\n2、互卦\n3、变卦\n4、综卦\n5、错卦\n6、不需要：\n'))
            if answer != 6:
                if answer == 1:
                    print('\n{}主体：\n' .format(G64(BG_up, BG_down)))
                    Search_txt(G64(BG_up, BG_down))
                    print('----------------------------')
                    Search_line(G64(BG_up, BG_down), num_yao)
                    print('----------------------------')

                elif answer == 2:
                    print('\n{}主体：\n'.format(G64(H_up, H_down)))
                    Search_txt(G64(H_up, H_down))
                elif answer == 3:
                    print('\n{}主体：\n'.format(G64(B_up, B_down)))
                    Search_txt(G64(B_up, B_down))
                elif answer == 4:
                    print('\n{}主体：\n'.format(G64(Z_up, Z_down)))
                    Search_txt(G64(Z_up, Z_down))
                elif answer == 5:
                    print('\n{}主体：\n'.format(G64(C_up, C_down)))
                    Search_txt(G64(C_up, C_down))

                if n_ymdh == 6 or n_ymdh == 12 or n_ymdh == 0:
                    Search_last(G64(BG_up, BG_down))



            else:
                break
        except ValueError:
            print('输入错误，请重新输入！')
            continue

    try:
        save = int(input('\n需要打印到该文件所在文件夹请输入1，不需要请随意输入其他数字然后回车，等待五秒返回菜单：\n'))
    except ValueError:
        save = 0

    if save == 1:

        sa = open('梅花结果.txt', 'a+', encoding='utf-8')
        sa.read()
        sa.write('\n')
        sa.write(create_time)
        sa.write('\n')
        sa.write(nong)
        sa.write('\n')
        sa.write('\n—上卦:%s—\t—下卦:%s—\n\t———动爻为%s———\n' % (BG_up, BG_down, num_yao))
        sa.write('上卦属性：%s\t下卦属性：%s\n' % (BG_sx(BG_up), BG_sx(BG_down)))
        sa.write('上卦类属：%s\t下卦类属：%s\n\n' % (BG_ls(BG_up), BG_ls(BG_down)))
        sa.write('\n体：%s\t\t用：%s\n' % (TY_pd('t'), TY_pd('y')))
        sa.write(TY())
        sa.write('\n')
        sa.write('\n本卦：%s\n' % (G64(BG_up, BG_down)))
        sa.write('%s\n%s\n\n' % (BG_line(BG_up), BG_line(BG_down)))
        sa.write('互卦：%s\n' % (G64(H_up, H_down)))
        sa.write('%s\n%s\n\n' % (BG_line(H_up), BG_line(H_down)))
        sa.write('变卦：%s\n' % (G64(B_up, B_down)))
        sa.write('%s\n%s\n\n' % (BG_line(B_up), BG_line(B_down)))
        sa.write('综卦：%s\n' % (G64(Z_up, Z_down)))
        sa.write('%s\n%s\n\n' % (BG_line(Z_up), BG_line(Z_down)))
        sa.write('错卦：%s\n' % (G64(C_up, C_down)))
        sa.write('%s\n%s\n' % (BG_line(C_up), BG_line(C_down)))

        sa.close()

    else:
        time.sleep(5)


if __name__ == '__main__':
    Main()