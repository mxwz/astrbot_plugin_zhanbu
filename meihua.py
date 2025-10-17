import re
import time
import random
import math
from datetime import datetime
from pathlib import Path

from zhdate import ZhDate
from typing import Iterable, List

# !/usr/local/sbin/python3
# -*- coding:utf-8 -*-

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
    diff = int(math.fabs(t)) - int(math.fabs(y))
    if diff == 1:
        return 1
    elif diff == -1:
        return -1
    elif diff == 2:
        return 2
    elif diff == -2:
        return -2
    elif diff == 3:
        return 3
    elif diff == -3:
        return -3
    elif diff == 4:
        return 4
    elif diff == -4:
        return -4
    else:
        # 注意：这里需要访问全局变量BG_up和BG_down，但在重构后应该通过参数传递
        return 5 if t == y else 6

# 0为比和，1为生我，-1为我生，2为克我，-2为我克，3为克我，-3为我克，4为我克，-4为克我，5为比劫，6为比助

def TY_pd(BG_up, BG_down, x, n):
    if x == 1:
        t = BG_down
        y = BG_up
        return t if n == 't' else y
    else:
        t = BG_up
        y = BG_down
        return t if n == 't' else y

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
        return '\t————\n\t————\n\t————'
    elif x == '兑':
        return '\t——  ——\n\t————\n\t————'
    elif x == '离':
        return '\t————\n\t——  ——\n\t————'
    elif x == '震':
        return '\t——  ——\n\t——  ——\n\t————'
    elif x == '巽':
        return '\t————\n\t————\n\t——  ——'
    elif x == '坎':
        return '\t——  ——\n\t————\n\t——  ——'
    elif x == '坤':
        return '\t——  ——\n\t——  ——\n\t——  ——'
    else:
        return '\t————\n\t——  ——\n\t——  ——'

def yao(x):
    if x == '阴':
        return '——  ——'
    else:
        return '————'

def yao_3(x, y, z):
    if x == '————' and y == '————' and z == '————':
        return '乾'
    elif x == '——  ——' and y == '————' and z == '————':
        return '兑'
    elif x == '————' and y == '——  ——' and z == '————':
        return '离'
    elif x == '——  ——' and y == '——  ——' and z == '————':
        return '震'
    elif x == '————' and y == '————' and z == '——  ——':
        return '巽'
    elif x == '——  ——' and y == '————' and z == '——  ——':
        return '坎'
    elif x == '————' and y == '——  ——' and z == '——  ——':
        return '艮'
    else:
        return '坤'

def yao_4(x):
    mapping = {
        '乾': ['阳', '阳', '阳'],
        '兑': ['阴', '阳', '阳'],
        '离': ['阳', '阴', '阳'],
        '震': ['阴', '阴', '阳'],
        '巽': ['阳', '阳', '阴'],
        '坎': ['阴', '阳', '阴'],
        '艮': ['阳', '阴', '阴'],
        '坤': ['阴', '阴', '阴']
    }
    return mapping.get(x, ['阳', '阴', '阴'])

def yao_fan(x):
    if x == '阴':
        return '阳'
    else:
        return '阴'

def yao_fan_yy(x):
    if x == '——  ——':
        return '————'
    else:
        return '——  ——'

# 定义体用关系
def TY(BG_up, BG_down, x):
    t = TY_pd(BG_up, BG_down, x, 't')
    y = TY_pd(BG_up, BG_down, x, 'y')

    t_wx = BG_sx(t)
    y_wx = BG_sx(y)

    sk_result = SK(wx_num(t_wx), wx_num(y_wx))

    if sk_result == 1:
        return '----用生体----'
    elif sk_result == -1:
        return '----体生用----'
    elif sk_result == 2:
        return '----用克体----'
    elif sk_result == -2:
        return '----体克用----'
    elif sk_result == 3:
        return '----体克用----'
    elif sk_result == -3:
        return '----用克体----'
    elif sk_result == 4:
        return '----体生用----'
    elif sk_result == -4:
        return '----用生体----'
    elif sk_result == 5:
        return '----体用比劫----'
    else:
        return '----体用比助----'

# 时间起数
def time_divination(time_dz_func):
    # 新历农历转换
    create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 新历年月日
    year = int(create_time[0:4])
    mouth = int(create_time[5:7])
    day = int(create_time[8:10])

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

    n_year_num = (n_year % 60) - 3
    n_ymd = n_year_num + n_mouth + n_day
    n_ymdh = n_ymd + time_dz_func()

    num_up = n_ymd
    num_down = n_ymdh
    num_yao = n_ymdh % 6
    if num_yao == 0:
        num_yao = 6

    return num_up, num_down, num_yao

# 笔画起数（仅支持两字到六字）
def stroke_divination(chars_strokes, sc):
    num_up = 0
    num_down = 0

    if len(chars_strokes) % 2 == 0:  # 判断偶数
        # 偶数下，均衡分配
        num_up = sum(chars_strokes[:(len(chars_strokes) // 2)])
        num_down = sum(chars_strokes[(len(chars_strokes) // 2):])
    else:
        # 奇数前少后多相差1
        num_up = sum(chars_strokes[:(len(chars_strokes) // 2)])
        num_down = sum(chars_strokes[(len(chars_strokes) // 2):])

    # 获取时辰地支序号
    hour = int(time.strftime('%H', time.localtime(time.time())))

    if sc:
        time_dz = sc
    else:
        time_dz = dizhi(hour)
    sc_num = get_sc_num(time_dz)

    num_yao = (num_up + num_down + sc_num) % 6
    if num_yao == 0:
        num_yao = 6

    return num_up, num_down, num_yao

# 随机数字起数
def random_divination(count, sc):
    if not 2 <= count <= 6:
        raise ValueError("数字个数必须在2-6之间")

    numbers = [random.randint(1, 20) for _ in range(count)]

    num_up = 0
    num_down = 0

    if len(numbers) % 2 == 0:  # 判断偶数
        # 偶数下，均衡分配
        num_up = sum(numbers[:(len(numbers) // 2)])
        num_down = sum(numbers[(len(numbers) // 2):])
    else:
        # 奇数前少后多相差1
        num_up = sum(numbers[:(len(numbers) // 2)])
        num_down = sum(numbers[(len(numbers) // 2):])

    # 获取时辰地支序号
    hour = int(time.strftime('%H', time.localtime(time.time())))
    if sc:
        time_dz = sc
    else:
        time_dz = dizhi(hour)
    sc_num = get_sc_num(time_dz)

    num_yao = (num_up + num_down + sc_num) % 6
    if num_yao == 0:
        num_yao = 6

    return num_up, num_down, num_yao

# 自定义数字起数
def custom_divination(numbers, sc):
    if len(numbers) < 2 or len(numbers) > 6:
        raise ValueError("数字个数必须在2-6之间")

    for num in numbers:
        if num <= 0:
            raise ValueError("所有数字必须为正整数")

    num_up = 0
    num_down = 0

    if len(numbers) % 2 == 0:  # 判断偶数
        # 偶数下，均衡分配
        num_up = sum(numbers[:(len(numbers) // 2)])
        num_down = sum(numbers[(len(numbers) // 2):])
    else:
        # 奇数前少后多相差1
        num_up = sum(numbers[:(len(numbers) // 2)])
        num_down = sum(numbers[(len(numbers) // 2):])

    # 获取时辰地支序号
    hour = int(time.strftime('%H', time.localtime(time.time())))
    if sc:
        time_dz = sc
    else:
        time_dz = dizhi(hour)
    sc_num = get_sc_num(time_dz)

    num_yao = (num_up + num_down + sc_num) % 6
    if num_yao == 0:
        num_yao = 6

    return num_up, num_down, num_yao

# 三数起数（第一个数字为上卦，第二个数字为下卦，第三个数字为动爻）
def three_num_divination(num_up, num_down, num_yao_base, use_shichen=True, sc=None):
    if use_shichen:
        # 获取时辰地支序号
        hour = int(time.strftime('%H', time.localtime(time.time())))
        if sc:
            time_dz = sc
        else:
            time_dz = dizhi(hour)
        sc_num = get_sc_num(time_dz)
        num_yao = (num_yao_base + sc_num) % 6
    else:
        num_yao = num_yao_base % 6

    if num_yao == 0:
        num_yao = 6

    return num_up, num_down, num_yao

# 地支序号
def get_sc_num(time_dz):
    mapping = {
        '子': 1,
        '丑': 2,
        '寅': 3,
        '卯': 4,
        '辰': 5,
        '巳': 6,
        '午': 7,
        '未': 8,
        '申': 9,
        '酉': 10,
        '戌': 11,
        '亥': 12
    }
    return mapping.get(time_dz, 1)

def calculate_gua_xiang(num_up, num_down, num_yao):
    BG_up = xiantian(num_up)
    BG_down = xiantian(num_down)

    x = 1 if num_yao > 3 else 0  # 下卦为体，上卦为用

    # [0:6] 本卦总阴阳yy_1
    yy_1 = yao_4(BG_up) + yao_4(BG_down)

    # 本卦阴阳转换图像
    yy_1_2 = [yao(i) for i in yy_1]

    # 互卦的阴阳
    H_up_1 = yy_1[1:4]
    H_down_1 = yy_1[2:5]
    # 互卦的图像
    H_up_2 = yy_1_2[1:4]
    H_down_2 = yy_1_2[2:5]
    # 互卦组合
    H_up = yao_3(H_up_2[0], H_up_2[1], H_up_2[2])
    H_down = yao_3(H_down_2[0], H_down_2[1], H_down_2[2])

    # 变卦总阴阳yy_b
    yy_b = yy_1.copy()
    yy_b.reverse()
    m_1 = yy_b.pop(num_yao - 1)
    yy_b.insert(num_yao - 1, yao_fan(m_1))
    yy_b.reverse()
    # 变卦阴阳转图像
    yy_b_2 = [yao(i) for i in yy_b]
    # 变卦组合
    B_up = yao_3(yy_b_2[0], yy_b_2[1], yy_b_2[2])
    B_down = yao_3(yy_b_2[3], yy_b_2[4], yy_b_2[5])

    # 综卦分解
    b_up_2 = yy_1_2[0:3]
    b_down_2 = yy_1_2[3:6]
    # 综卦上分解
    Z_up_x = yao_fan_yy(b_up_2[0])
    Z_up_y = yao_fan_yy(b_up_2[1])
    Z_up_z = yao_fan_yy(b_up_2[2])
    # 综卦下分解
    Z_down_x = yao_fan_yy(b_down_2[0])
    Z_down_y = yao_fan_yy(b_down_2[1])
    Z_down_z = yao_fan_yy(b_down_2[2])
    # 综卦组合
    Z_up = yao_3(Z_up_x, Z_up_y, Z_up_z)
    Z_down = yao_3(Z_down_x, Z_down_y, Z_down_z)

    # 错卦总阴阳
    C_1 = yy_1.copy()
    C_1.reverse()
    # 错卦总图像
    C_2 = yy_1_2.copy()
    C_2.reverse()
    # 错卦组合
    C_up = yao_3(C_2[0], C_2[1], C_2[2])
    C_down = yao_3(C_2[3], C_2[4], C_2[5])

    # 构建返回结果
    result = []

    # 添加卦象信息字符串
    bengua_str = f'本卦：{G64(BG_up, BG_down)}\n{BG_line(BG_up)}\n{BG_line(BG_down)}'
    hugua_str = f'互卦：{G64(H_up, H_down)}\n{BG_line(H_up)}\n{BG_line(H_down)}'
    biangua_str = f'变卦：{G64(B_up, B_down)}\n{BG_line(B_up)}\n{BG_line(B_down)}'
    zonggua_str = f'综卦：{G64(Z_up, Z_down)}\n{BG_line(Z_up)}\n{BG_line(Z_down)}'
    cuogua_str = f'错卦：{G64(C_up, C_down)}\n{BG_line(C_up)}\n{BG_line(C_down)}'

    # 添加其他信息到列表
    info_list = [
        f"""—上卦:{BG_up}—\t—下卦:{BG_down}—\n\t———动爻为{num_yao}———
\n上卦属性：{BG_sx(BG_up)}\t下卦属性：{BG_sx(BG_down)}
\n上卦类属：{BG_ls(BG_up)}\t下卦类属：{BG_ls(BG_down)}
\n体：{TY_pd(BG_up, BG_down, x, "t")}\t\t\t用：{TY_pd(BG_up, BG_down, x, "y")}
\n{TY(BG_up, BG_down, x)}"""
    ]

    result.append(bengua_str)
    result.append(hugua_str)
    result.append(biangua_str)
    result.append(zonggua_str)
    result.append(cuogua_str)
    result.extend(info_list)

    return result

chinese_char_map = {}
# 获取当前文件的路径
current_file_path = Path(__file__).resolve()
# 获取当前文件所在的目录
current_dir = current_file_path.parent
with open(f'{current_dir}/chinese_unicode_table.txt', 'r', encoding='UTF-8') as f:
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


dict1 = {}
# 数字提取
with open(f'{current_dir}/htmlnum.txt', 'r') as f:
    lines = f.readlines()  # 逐行读取文件内容，保存为一个列表
nums = []  # 初始化一个空列表，用于存放提取出的数字
for line in lines:
    line = line.strip()  # 去除每行的空白和换行符
    if line.isdigit():  # 判断当前行是否为数字
        nums.append(int(line))  # 将当前行的数字转为整数，并添加到列表中
# 文字提取
with open(f'{current_dir}/cash.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()  # 逐行读取文件内容，保存为一个列表
lst = []  # 初始化一个空列表，用于存储转换后的字符串
for line in lines:
    s = line.strip()  # 去除每行的空白字符和换行符
    if s:  # 判断处理后的内容是否为空或空白字符
        lst.append(s)  # 将非空的内容添加到列表中
# 卦象对应的文件名装入字典
for i in range(64):
    dict1[lst[i]] = nums[i]
def Search_txt(x):
    with open(f'{current_dir}/64/%d.txt' % (dict1[x]), 'r', encoding='utf-8') as file:
        content = ''
        start = False  # 标志是否匹配到了"传统解卦"
        for line in file:
            if re.search(r'传统解卦', line):
                start = True  # 匹配到关键字后开始保存
            if start:
                content += line  # 拼接累计读取的行
            if re.search(r'决策', line):
                break  # 匹配到第二个关键字，跳出循环
    return content
def Search_line(x, y):
    with open(f'{current_dir}/64/%d.txt' % (dict1[x]), 'r', encoding='utf-8') as file:
        content = ''
        start = False  # 标志是否匹配到了"传统解卦"
        for line in file:
            if re.search(r'--%s--' % str(y), line):
                start = True  # 匹配到关键字后开始保存
            if start:
                content += line  # 拼接累计读取的行
            if re.search(r'--%s--' % str(y+1), line):
                break  # 匹配到第二个关键字，跳出循环
    return content


def Meihua(question, gender, method, **kwargs):
    """
    梅花易数起卦主函数

    Args:
        question: 问题
        gender: 性别
        method: 起数方式 (1-5)
        **kwargs: 其他参数，根据method不同而不同

    Returns:
        list: 包含卦象字符串和其他信息的列表
    """

    try:
        if method == 1:  # 时间起数
            # 获取时辰地支序号函数
            def time_dz_func():
                hour = int(time.strftime('%H', time.localtime(time.time())))
                time_dz = dizhi(hour)
                return get_sc_num(time_dz)

            num_up, num_down, num_yao = time_divination(time_dz_func)

        elif method == 2:  # 笔画起数
            chars = kwargs.get('chars', [])
            sc = kwargs.get('sc', None)
            if not 2 <= len(chars) <= 6:
                raise ValueError("字符数必须在2-6之间")

            chars_strokes = []
            for i in chars:
                n = __sort_by_strokes_core(i)
                chars_strokes.append(n)
            num_up, num_down, num_yao = stroke_divination(chars_strokes, sc)

        elif method == 3:  # 随机数字起数
            count = kwargs.get('count', 3)
            sc = kwargs.get('sc', None)
            num_up, num_down, num_yao = random_divination(count, sc)

        elif method == 4:  # 自定义数字起数
            numbers = kwargs.get('numbers', [])
            sc = kwargs.get('sc', None)
            num_up, num_down, num_yao = custom_divination(numbers, sc)

        elif method == 5:  # 三数起数
            num_up = kwargs.get('num_up', 0)
            num_down = kwargs.get('num_down', 0)
            num_yao_base = kwargs.get('num_yao_base', 0)
            use_shichen = kwargs.get('use_shichen', True)
            sc = kwargs.get('sc', None)
            num_up, num_down, num_yao = three_num_divination(num_up, num_down, num_yao_base, sc, use_shichen)

        else:
            raise ValueError("无效的起数方式")

        # 计算卦象并返回结果
        return [f"问题：{question}", f"性别：{gender}"] + calculate_gua_xiang(num_up, num_down, num_yao)

    except Exception as e:
        return [f"起卦过程中发生错误: {str(e)}"]

# 示例用法注释：
# result = main("我的事业如何？", "男", 1)  # 时间起数
# result = main("我的事业如何？", "男", 2, chars=["李", "明"])  # 笔画起数
# result = main("我的事业如何？", "男", 3, count=3)  # 随机数字起数
# result = Meihua("我的事业如何？", "男", 4, numbers=[100, 12, 35, 14, 25, 46])  # 自定义数字起数
# result = main("我的事业如何？", "男", 5, num_up=10, num_down=20, num_yao_base=3, use_shichen=True)  # 三数起数

if __name__ == '__main__':
    # 为了保持原文件可运行，添加一个简单的测试调用
    # 在实际使用中，应该通过main函数调用
    # print("这是一个优化后的梅花易数模块，可以通过调用main()函数使用")
    a = Meihua("我的事业如何？", "男", 4, numbers=[100, 12, 35, 14, 25, 46])
    for i in a:
        print(i)