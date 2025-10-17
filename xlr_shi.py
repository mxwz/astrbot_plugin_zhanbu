import random
import time
import math
from pathlib import Path

from zhdate import ZhDate
from datetime import datetime
import json, os

# print('保存')

def exists_path():
    if not os.path.exists('./日志管理/'):
        os.makedirs('./日志管理/')

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()
# 获取当前文件所在的目录
current_dir = current_file_path.parent

# 存放报数
list1 = []
# 存放六神
list2 = []
# 存放五行
list3 = []
# 存放长生
list4 = []

list5 = []

list6 = []
dict1 = {}

hls_zd = {}

hls_zd_2 = {}

s = 1

hourList = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
hourlist = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

num_str = ['大安', '留连', '速喜', '赤口', '小吉', '空亡']  # 已用
num_str_1 = ['大安', '留连', '速喜', '赤口', '小吉', '空亡']  # 已用
num_str_2 = ['大安', '留连', '速喜', '赤口', '小吉', '空亡']  # 已用
num_str_3 = ['大安', '留连', '速喜', '赤口', '小吉', '空亡']  # 排地支
hourlist_3 = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']


# 排盘用
pan_1 = ['大安', '留连', '速喜', '赤口', '小吉', '空亡']
pan_2 = ['青龙', '腾蛇', '朱雀', '白虎', '玄武', '勾陈']
pan = {'子':'玄武', '丑':'勾陈', '寅':'青龙', '卯':'青龙', '辰':'勾陈', '巳':'朱雀', '午':'朱雀', '未':'腾蛇', '申':'白虎', '酉':'白虎', '戌':'腾蛇', '亥':'玄武'}
pan_list = {}
pan_Y = ['子','寅','午','申','辰','戌']
pan_Y_num = [1,3,5,7,9,11]


num_index = ['青龙', '腾蛇', '朱雀', '白虎', '玄武', '勾陈']
wx = ['木', '火', '土', '金', '水']
hls = ['青龙', '朱雀', '勾陈', '白虎', '玄武', '腾蛇']

cs_1 = {'金': '死', '木': '沐浴', '水': '帝旺', '火': '胎', '土': '帝旺'}
cs_2 = {'金': '墓', '木': '冠带', '水': '衰', '火': '养', '土': '衰'}
cs_3 = {'金': '绝', '木': '临官', '水': '病', '火': '长生', '土': '病'}
cs_4 = {'金': '胎', '木': '帝旺', '水': '死', '火': '沐浴', '土': '死'}
cs_5 = {'金': '养', '木': '衰', '水': '墓', '火': '冠带', '土': '墓'}
cs_6 = {'金': '长生', '木': '病', '水': '绝', '火': '临官', '土': '绝'}
cs_7 = {'金': '沐浴', '木': '死', '水': '胎', '火': '帝旺', '土': '胎'}
cs_8 = {'金': '冠带', '木': '墓', '水': '养', '火': '衰', '土': '养'}
cs_9 = {'金': '临官', '木': '绝', '水': '长生', '火': '病', '土': '长生'}
cs_10 = {'金': '帝旺', '木': '胎', '水': '沐浴', '火': '死', '土': '沐浴'}
cs_11 = {'金': '衰', '木': '养', '水': '冠带', '火': '墓', '土': '冠带'}
cs_12 = {'金': '病', '木': '长生', '水': '临官', '火': '绝', '土': '临官'}
list4.append(cs_1)
list4.append(cs_2)
list4.append(cs_3)
list4.append(cs_4)
list4.append(cs_5)
list4.append(cs_6)
list4.append(cs_7)
list4.append(cs_8)
list4.append(cs_9)
list4.append(cs_10)
list4.append(cs_11)
list4.append(cs_12)

list5.append(cs_1)
list5.append(cs_2)
list5.append(cs_3)
list5.append(cs_4)
list5.append(cs_5)
list5.append(cs_6)
list5.append(cs_7)
list5.append(cs_8)
list5.append(cs_9)
list5.append(cs_10)
list5.append(cs_11)
list5.append(cs_12)




def bagua(x):
    global bg_text
    with open(f'{current_dir}/8/{x}.txt','r',encoding='utf-8') as f:
        bg_text = f.read()

    text = f"""{bg_text}
--------\n
    """

    return text

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


def dz_num_p(x):
    if x == 2:
        return '丑'
    elif x == 3:
        return '寅'
    elif x == 4:
        return '卯'
    elif x == 5:
        return '辰'
    elif x == 6:
        return '巳'
    elif x == 7:
        return '午'
    elif x == 8:
        return '未'
    elif x == 9:
        return '申'
    elif x == 10:
        return '酉'
    elif x == 11:
        return '戌'
    elif x == 12:
        return '亥'
    else:
        return '子'

def dizhi_wx(shichen):
    if 1 <= shichen < 3:
        return '土'
    elif 3 <= shichen < 5:
        return '木'
    elif 5 <= shichen < 7:
        return '木'
    elif 7 <= shichen < 9:
        return '土'
    elif 9 <= shichen < 11:
        return '火'
    elif 11 <= shichen < 13:
        return '火'
    elif 13 <= shichen < 15:
        return '土'
    elif 15 <= shichen < 17:
        return '金'
    elif 17 <= shichen < 19:
        return '金'
    elif 19 <= shichen < 21:
        return '土'
    elif 21 <= shichen < 23:
        return '水'
    else:
        return '水'


def dizhi2_wx(shichen):
    if shichen == 2:
        return '土'
    elif shichen == 3:
        return '木'
    elif shichen == 4:
        return '木'
    elif shichen == 5:
        return '土'
    elif shichen == 6:
        return '火'
    elif shichen == 7:
        return '火'
    elif shichen == 8:
        return '土'
    elif shichen == 9:
        return '金'
    elif shichen == 10:
        return '金'
    elif shichen == 11:
        return '土'
    elif shichen == 12:
        return '水'
    else:
        return '水'


def dizhi_wx_2(x):
    if x == 2:
        return '土'
    elif x == 3:
        return '木'
    elif x == 4:
        return '木'
    elif x == 5:
        return '土'
    elif x == 6:
        return '火'
    elif x == 7:
        return '火'
    elif x == 8:
        return '土'
    elif x == 9:
        return '金'
    elif x == 10:
        return '金'
    elif x == 11:
        return '土'
    elif x == 12:
        return '水'
    else:
        return '水'


def Sc_num(x):
    if x == '丑':
        return 2
    elif x == '寅':
        return 3
    elif x == '卯':
        return 4
    elif x == '辰':
        return 5
    elif x == '巳':
        return 6
    elif x == '午':
        return 7
    elif x == '未':
        return 8
    elif x == '申':
        return 9
    elif x == '酉':
        return 10
    elif x == '戌':
        return 11
    elif x == '亥':
        return 12
    else:
        return 1


def dizhi_sx(shichen):
    if 1 <= shichen < 3:
        return '阴'
    elif 3 <= shichen < 5:
        return '阳'
    elif 5 <= shichen < 7:
        return '阴'
    elif 7 <= shichen < 9:
        return '阳'
    elif 9 <= shichen < 11:
        return '阴'
    elif 11 <= shichen < 13:
        return '阳'
    elif 13 <= shichen < 15:
        return '阴'
    elif 15 <= shichen < 17:
        return '阳'
    elif 17 <= shichen < 19:
        return '阴'
    elif 19 <= shichen < 21:
        return '阳'
    elif 21 <= shichen < 23:
        return '阴'
    else:
        return '阳'


def BG(x, y, z):
    if x == '阳' and y == '阳' and z == '阳':
        return '乾'
    elif x == '阴' and y == '阴' and z == '阴':
        return '坤'
    elif x == '阳' and y == '阴' and z == '阴':
        return '艮'
    elif x == '阴' and y == '阳' and z == '阴':
        return '坎'
    elif x == '阳' and y == '阳' and z == '阴':
        return '巽'
    elif x == '阴' and y == '阴' and z == '阳':
        return '震'
    elif x == '阳' and y == '阴' and z == '阳':
        return '离'
    else:
        return '兑'


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


def Sc_yy(x):
    if x in pan_Y or pan_Y_num:
        return '阳'
    else:
        return '阴'

# 定义六神函数
def sixgod(x):
    if x % 6 == 1:
        return num_str[0]
    elif x % 6 == 2:
        return num_str[1]
    elif x % 6 == 3:
        return num_str[2]
    elif x % 6 == 4:
        return num_str[3]
    elif x % 6 == 5:
        return num_str[4]
    else:
        return num_str[6]


def ls_yy(x):
    if x == '大安':
        return '阳'
    elif x == '速喜':
        return '阳'
    elif x == '小吉':
        return '阳'
    else:
        return '阴'


def hls_yy(x):
    if x == '朱雀':
        return '阳'
    elif x == '青龙':
        return '阳'
    elif x == '勾陈':
        return '阳'
    else:
        return '阴'


# x3
def sixgod_sx(x):
    if x == '留连':
        return '阴'
    elif x == '赤口':
        return '阴'
    # 此处做出了更改，将赤口属性调为阴
    elif x == '空亡':
        return '阴'
    else:
        return '阳'

# def HLS_sx2(x):
#     if x == '亥':
#         return '阴'
#     else:
#         return '阳'


def six_five(x):
    if x == '大安':
        return wx[0]
    elif x == '小吉':
        return wx[4]
    elif x == '赤口':
        return wx[3]
    elif x == '速喜':
        return wx[1]
    else:
        return wx[2]


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


def MK():
    if x3 == '大安' and time_dz == '未':
        return '---入墓---'
    elif x3 == '速喜' and time_dz == '戌':
        return '---入墓---'
    elif x3 == '赤口' and time_dz == '丑':
        return '---入墓---'
    elif (x3 == '小吉' or x3 == '空亡' or x3 == '留连') and time_dz == '辰':
        return '---入墓---'
    else:
        return '\t'


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
        if sixgod_sx(x3) == dizhi_sx(hour):
            return 5
        else:
            return 6


def SK_pan(t, y):
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

        return 5


def LQ(x,y):  # x和y是时辰转换的数字
    if SK_pan(wx_num(dizhi_wx_2(x)), wx_num(dizhi_wx_2(y))) == 1:
        return '父母'
    elif SK_pan(wx_num(dizhi_wx_2(x)), wx_num(dizhi_wx_2(y))) == -1:
        return '子孙'
    elif SK_pan(wx_num(dizhi_wx_2(x)), wx_num(dizhi_wx_2(y))) == 2:
        return '官鬼'
    elif SK_pan(wx_num(dizhi_wx_2(x)), wx_num(dizhi_wx_2(y))) == -2:
        return '妻财'
    elif SK_pan(wx_num(dizhi_wx_2(x)), wx_num(dizhi_wx_2(y))) == 3:
        return '妻财'
    elif SK_pan(wx_num(dizhi_wx_2(x)), wx_num(dizhi_wx_2(y))) == -3:
        return '官鬼'
    elif SK_pan(wx_num(dizhi_wx_2(x)), wx_num(dizhi_wx_2(y))) == 4:
        return '子孙'
    elif SK_pan(wx_num(dizhi_wx_2(x)), wx_num(dizhi_wx_2(y))) == -4:
        return '父母'
    elif SK_pan(wx_num(dizhi_wx_2(x)), wx_num(dizhi_wx_2(y))) == 5:
        return '兄弟'
    else:
        return '自身'


# 体生用，体克用，用生体，用克体，体用比助，体用比劫
# 0为比和，1为生我，-1为我生，2为克我，-2为我克，3为克我，-3为我克，4为我生，-4为生我，5为比劫，6为比助
# y3为落宫五行，dz_wx为时辰五行
def TY():
    if SK(wx_num(y3), wx_num(dizhi_wx(hour))) == 1:
        return '----用生体----'
    elif SK(wx_num(y3), wx_num(dizhi_wx(hour))) == -1:
        return '----体生用----'
    elif SK(wx_num(y3), wx_num(dizhi_wx(hour))) == 2:
        return '----用克体----'
    elif SK(wx_num(y3), wx_num(dizhi_wx(hour))) == -2:
        return '----体克用----'
    elif SK(wx_num(y3), wx_num(dizhi_wx(hour))) == 3:
        return '----体克用----'
    elif SK(wx_num(y3), wx_num(dizhi_wx(hour))) == -3:
        return '----用克体----'
    elif SK(wx_num(y3), wx_num(dizhi_wx(hour))) == 4:
        return '----体生用----'
    elif SK(wx_num(y3), wx_num(dizhi_wx(hour))) == -4:
        return '----用生体----'
    elif SK(wx_num(y3), wx_num(dizhi_wx(hour))) == 5:
        return '---体用比劫---'
    else:
        return '---体用比助---'


# 新历农历转换
create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# 新历年月日
year = int(create_time[0:4])
mouth = int(create_time[5:7])
day = int(create_time[8:10])
hourtime = int(create_time[11:13])
mintime = int(create_time[14:16])

if 24 > hourtime >= 23:
    hourtime = 00
    day += 1

# 新建新历
xin = datetime(year, mouth, day)
# 转换农历
nong = str(ZhDate.from_datetime(xin))
# 获取农历时辰
hour = int(time.strftime('%H', time.localtime(time.time())))
# 地支
time_dz = dizhi(hour)


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


def sc_num_2(x):
    if x == '子':
        return 1
    elif x == '丑':
        return 2
    elif x == '寅':
        return 3
    elif x == '卯':
        return 4
    elif x == '辰':
        return 5
    elif x == '巳':
        return 6
    elif x == '午':
        return 7
    elif x == '未':
        return 8
    elif x == '申':
        return 9
    elif x == '酉':
        return 10
    elif x == '戌':
        return 11
    else:
        return 12


# num_str_2.index(sixgod(sc_num()))
def HLS(x):
    num_str_1 = ['大安', '留连', '速喜', '赤口', '小吉', '空亡']
    for k in range(sc_num() - 1):
        y = num_str_1.pop(0)
        num_str_1.append(y)

    for i in num_str_1:
        hls_zd[i] = hls[0]
        z = hls.pop(0)
        hls.append(z)

    return hls_zd[x]


def LS_num(x):
    if x == '大安':
        return 1
    elif x == '留连':
        return 2
    elif x == '速喜':
        return 3
    elif x == '赤口':
        return 4
    elif x == '小吉':
        return 5
    else:
        return 6


def CS(x):
    return list4[sc_num() - 1][x]


def NI(x):
    if x == '子':
        return 23
    elif x == '丑':
        return 1
    elif x == '寅':
        return 3
    elif x == '卯':
        return 5
    elif x == '辰':
        return 7
    elif x == '巳':
        return 9
    elif x == '午':
        return 11
    elif x == '未':
        return 13
    elif x == '申':
        return 15
    elif x == '酉':
        return 17
    elif x == '戌':
        return 19
    else:
        return 21

def LQ_random(x):  # x为装着最后六神的列表
    # 先排地支:确定自身（最后一个六神），再确定隔位顺排
    global zz
    global zzz
    global a_str
    global b_str
    for k in range(LS_num(x) - 1):
        x_x = num_str_3.pop(0)
        num_str_3.append(x_x)
    for k in range(sc_num() - 1):
        x_y = hourlist_3.pop(0)
        hourlist_3.append(x_y)
    ge = hourlist_3[::2]
    # gege = ge
    # print(ge)

    # 定六神
    for i in range(6):
        zzz = num_str_3[i]  # 六神
        zz = ge[i]  # 地支
        dict1[zzz] = zz
        pan_list[zzz] = zz

        dict1[zzz] = pan[zz]
    # print(pan_list)
    # print(dict1)

    for i in pan_list:
        pan_list[i] = LQ(Sc_num(ge[0]), (Sc_num(pan_list[i])))
        # print(pan_list)

    for i in pan_list:
        pan_list[i] = '自身'
        if pan_list[i] == '自身':
            break

    # 用一个集合来保存已经出现过的值
    seen_values = set()

    for key, value in pan_list.items():
        if value in seen_values:
            # 如果这个值已经出现过，那么将第一个出现的值的键改为其他值
            for key2, value2 in pan_list.items():
                if value2 == value:
                    pan_list[key2] = '兄弟'
                    break
            break
        else:
            seen_values.add(value)

    a_str = json.dumps(pan_list)
    a_str = a_str.replace('{', '').replace('}', '').replace('"', '').replace(' ', '').replace(',', '    ').rstrip()
    a_str = bytes(a_str, 'utf-8').decode('unicode_escape')

    b_str = json.dumps(dict1)
    b_str = b_str.replace('{', '').replace('}', '').replace('"', '').replace(' ', '').replace(',', '    ').rstrip()
    b_str = bytes(b_str, 'utf-8').decode('unicode_escape')

    text = f"""\n---排盘信息：---\n
{a_str}

{b_str}
    """

    return a_str, b_str, text

    # print(pan_list)


def is_zodiac_character(char, choice = False, extract = False):
    zodiac_characters = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    if extract:
        return "".join([element for element in zodiac_characters if element in char])
    if not choice:
        return char in zodiac_characters
    elif choice:
        return any(element in char for element in zodiac_characters)


def xiaoliuren(msg: str):
    # 提出问题
    # 3.时间(00:00)四数起；
    global a_str, c, number_list
    global b_str
    global time_dz
    global x3
    # global dz_sx
    global y3
    # global dz_wx
    global num_3
    global hour
    global list1

    # 例如：/小六壬 [问题] [选项(数字)] [数字(英文逗号)] [时辰(单字)] [详细/简短(default 0 or 1)]
    # 例如：/小六壬 财运 1
    # 例如：/小六壬 财运 2
    # 例如：/小六壬 财运 3 1,2,3
    msg_list = msg.split(' ')

    if len(msg_list) <= 2:
        return "输入维度有误"

    command = msg_list[0]
    problem = msg_list[1]
    try:
        choice = int(msg_list[2])
    except ValueError as e:
        return "选项输入错误，请规范输入"

    if choice != 3:
        try:
            if ',' in msg_list[3]:
                return "该选项不能输入自定义数字，请删除选项后的数字列表"
        except IndexError as e:
            pass

    if len(msg_list) < 4 and choice == 3:
        return "输入维度有误"
    if len(msg_list) >= 4 and choice == 3:
        number = msg_list[3]
        try:
            number_list = list(map(int, number.split(',')))
            # print(number_list)
        except Exception as e:
            return f"起课数字输入错误，请规范输入：{e}"


    if len(msg_list) == 5 or is_zodiac_character(msg, True):
        try:
            time_dz = is_zodiac_character(msg, extract=True)
            # print(time_dz)
            if not is_zodiac_character(time_dz):
                if choice == 3:
                    time_dz = dizhi(hour)
                else:
                    return "时辰不规范（请按照子，丑，寅等单字输入）"
            hour = NI(time_dz)
        except Exception as f:
            return f

    # c = msg_list[5]
    c = 0 if "简短" in msg_list else 1
    # print(c)


    if len(msg_list) < 3:
        return "维度错误"


    # choice = int(input('请选择：1.随机抽取；2.时间定数；3.自行输入：\n'))

    if choice == 1:
        num_1 = random.randint(1, 6)
        # 随机生成1-6范围内（含1和6）的一个整数，并赋值给变量a
        num_2 = random.randint(1, 6)
        num_3 = random.randint(1, 6)

        list1.append(num_1)
        list1.append(num_2)
        list1.append(num_3)

        # time.sleep(1)
        # print(num_1)
        # time.sleep(1)
        # print(num_2)
        # time.sleep(1)
        # print(num_3)

    elif choice == 2:
        if is_zodiac_character(msg, True):
            return "时辰起课不能换时辰，请删除时辰后再试"
        # 获取农历月日
        if nong[7].isdigit():  # 排除闰二月
            if nong[8].isdigit():  # 两位数月份
                num_1 = int(nong[7:9])
                # 日期：天
                if nong[11].isdigit():  # 二位数日期
                    num_2 = int(nong[10:12])
                else:  # 个位数日期
                    num_2 = int(nong[10])

            else:  # 一位数月份
                num_1 = int(nong[7])
                # 日期：天
                if nong[10].isdigit():  # 二位数日期
                    num_2 = int(nong[9:11])
                else:  # 个位数日期
                    num_2 = int(nong[9])

        else:  # 闰二月
            num_1 = int(nong[8])
            # 日期：天
            if nong[11].isdigit():  # 二位数日期
                num_2 = int(nong[10:12])
            else:  # 个位数日期
                num_2 = int(nong[10])

        # 返回值在十二生肖中的序号索引
        num_3 = int(hourlist.index(time_dz)) + 1
        # print('所得数字为%d,%d,%d' % (num_1, num_2, time_sx))
        list1.append(num_1)
        list1.append(num_2)
        list1.append(num_3)

    elif choice == 3:
        if len(number_list) != 3:
            return "数字请用英文逗号隔开，并且只容许三位，检查输入规范"
        num_1, num_2, num_3 = number_list
        list1 = number_list.copy()


    # 报数
    num_all = f"{str(num_1)}, {str(num_2)}, {str(num_3)}"

    # 按照数字获取相应六神
    for i in list1:
        for k in range(i - 1):
            x = num_str.pop(0)
            num_str.append(x)
        list2.append(num_str[0])

    # 分开六神，列表变为个体
    x1 = list2[0]
    x2 = list2[1]
    x3 = list2[2]

    # 根据六神分五行
    for i in list2:
        wuxing = six_five(i)
        list3.append(wuxing)

    # 分开五行，列表变为个体
    y1 = list3[0]
    y2 = list3[1]
    y3 = list3[2]

    # dz_wx = dizhi_wx(hour)
    # dz_sx = dizhi_sx(hour)

    x1_1 = ls_yy(x1)
    x2_1 = ls_yy(x2)
    x3_1 = ls_yy(x3)

    y1_1 = hls_yy(HLS(x1))
    y2_1 = hls_yy(HLS(x2))
    y3_1 = hls_yy(HLS(x3))

    '''更改内容:
    dz_wx,dz_sx
    dizhi_wx(hour), dizhi_sx(hour)
    '''

    # 输出最后排版
    if c == 0:
        texts = [f"""{create_time}
{nong}
问题：{problem}
报数：{num_all}
时辰：{time_dz}
{x1}  {x2}  {x3}
{y1}----{y2}----{y3}
{TY()}
{MK()}
"""]

    if c == 1:
        str_a, str_b, lq = LQ_random(x3)

        text1 = f"""{create_time}
{nong}
问题：{problem}
报数：{num_all}
时辰：{time_dz}
时辰五行：{dizhi_wx(hour)}
时辰阴阳：{dizhi_sx(hour)}
时辰排序：{sc_num()}
"""
        text2 = f"""
{x1}  {x2}  {x3}
{y1}----{y2}----{y3}
{ls_yy(x1)}----{ls_yy(x2)}----{ls_yy(x3)}
{CS(y1)}----{CS(y2)}----{CS(y3)}
{HLS(x1)}--{HLS(x2)}--{HLS(x3)}
{hls_yy(HLS(x1))}----{hls_yy(HLS(x2))}----{hls_yy(HLS(x3))}
{lq}
{TY()}
{MK()}
"""
        text3 = f"""
*****穿八卦*****
本卦：{BG(x1_1, x2_1, x3_1)}
类象：{BG_ls(BG(x1_1, x2_1, x3_1))}
属性：{BG_sx(BG(x1_1, x2_1, x3_1))}

客卦：{BG(y1_1, y2_1, y3_1)}
类象：{BG_ls(BG(y1_1, y2_1, y3_1))}
属性：{BG_sx(BG(y1_1, y2_1, y3_1))}
***************
本卦在下，客卦在上
"""
        text4 =  f"""
---本卦---
{bagua(BG(x1_1, x2_1, x3_1))}
"""
        text5 = f"""
---客卦---
{bagua(BG(y1_1, y2_1, y3_1))}
"""
        texts = [text1, text2, text3, text4, text5]
    return texts



if __name__ == '__main__':
    # exists_path()
    # /小六壬 [问题][选项(数字)][数字(英文逗号)][时辰(单字)][详细 / 简短(default 0 or 1)]
    a = xiaoliuren('/小六壬 财运 3 9,7,6 戌 简短')
    print(a)
