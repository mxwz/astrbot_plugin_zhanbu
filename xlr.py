#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/10/15 上午8:43
# @Author  : mxwz
# @Software: PyCharm
# @File    : xlr2.py
import random
import time
import math
from pathlib import Path

from zhdate import ZhDate
from datetime import datetime
import json, os

class XiaoLiuRen:
    def __init__(self):
        # 获取当前文件的路径
        self.current_file_path = Path(__file__).resolve()
        # 获取当前文件所在的目录
        self.current_dir = self.current_file_path.parent
        # 存放报数
        self.list1 = []
        # 存放六神
        self.list2 = []
        # 存放五行
        self.list3 = []

        self.num_str = ['大安', '留连', '速喜', '赤口', '小吉', '空亡']
        self.hourList = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
        self.hourlist = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        self.wx = ['木', '火', '土', '金', '水']
        self.hls = ['青龙', '腾蛇', '朱雀', '白虎', '玄武', '勾陈']

        # 长生十二宫
        self.cs_dict = {
            '金': ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养'],
            '木': ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养'],
            '水': ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养'],
            '火': ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养'],
            '土': ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养']
        }

        # 六神对应五行
        self.six_five_map = {
            '大安': '木',
            '小吉': '水',
            '赤口': '金',
            '速喜': '火',
            '留连': '土',
            '空亡': '土'
        }

        # 地支对应五行
        self.dizhi_wuxing = {
            '丑': '土', '寅': '木', '卯': '木', '辰': '土',
            '巳': '火', '午': '火', '未': '土', '申': '金',
            '酉': '金', '戌': '土', '亥': '水', '子': '水'
        }

        # 地支对应数字
        self.dizhi_number = {
            '丑': 2, '寅': 3, '卯': 4, '辰': 5,
            '巳': 6, '午': 7, '未': 8, '申': 9,
            '酉': 10, '戌': 11, '亥': 12, '子': 1
        }

        # 六神阴阳属性
        self.ls_yy_map = {
            '大安': '阳', '速喜': '阳', '小吉': '阳',
            '留连': '阴', '赤口': '阴', '空亡': '阴'
        }

        # 六神阴阳属性（另一种分类）
        self.hls_yy_map = {
            '朱雀': '阳', '青龙': '阳', '勾陈': '阳',
            '腾蛇': '阴', '白虎': '阴', '玄武': '阴'
        }

        # 八卦相关
        self.bg_map = {
            ('阳', '阳', '阳'): '乾', ('阴', '阴', '阴'): '坤',
            ('阳', '阴', '阴'): '艮', ('阴', '阳', '阴'): '坎',
            ('阳', '阳', '阴'): '巽', ('阴', '阴', '阳'): '震',
            ('阳', '阴', '阳'): '离', ('阴', '阳', '阳'): '兑'
        }

        self.bg_wuxing = {
            '乾': '金', '兑': '金', '离': '火',
            '震': '木', '巽': '木', '坎': '水',
            '坤': '土', '艮': '土'
        }

        self.bg_leixiang = {
            '乾': '天', '兑': '泽', '离': '火',
            '震': '雷', '巽': '风', '坎': '水',
            '坤': '地', '艮': '山'
        }

        # 排盘用
        self.pan = {
            '子':'玄武', '丑':'勾陈', '寅':'青龙', '卯':'青龙',
            '辰':'勾陈', '巳':'朱雀', '午':'朱雀', '未':'腾蛇',
            '申':'白虎', '酉':'白虎', '戌':'腾蛇', '亥':'玄武'
        }

        # 入墓判断
        self.mu_map = {
            '大安': '未', '速喜': '戌', '赤口': '丑'
        }

    def exists_path(self):
        """检查并创建日志目录"""
        if not os.path.exists('./日志管理/'):
            os.makedirs('./日志管理/')

    def bagua(self, x):
        """读取八卦内容"""
        try:
            with open(f'{self.current_dir}/8/{x}.txt', 'r', encoding='utf-8') as f:
                bg_text = f.read()
            return f"{bg_text}\n------------\n"
        except FileNotFoundError:
            return f"未找到八卦文件: {x}\n------------\n"

    def get_dizhi(self, shichen):
        """根据时辰获取地支"""
        ranges = [(1, 3, '丑'), (3, 5, '寅'), (5, 7, '卯'), (7, 9, '辰'),
                  (9, 11, '巳'), (11, 13, '午'), (13, 15, '未'), (15, 17, '申'),
                  (17, 19, '酉'), (19, 21, '戌'), (21, 23, '亥')]

        for start, end, dizhi in ranges:
            if start <= shichen < end:
                return dizhi
        return '子'

    def get_dizhi_wuxing(self, shichen):
        """根据时辰获取地支五行"""
        ranges = [(1, 3, '土'), (3, 5, '木'), (5, 7, '木'), (7, 9, '土'),
                  (9, 11, '火'), (11, 13, '火'), (13, 15, '土'), (15, 17, '金'),
                  (17, 19, '金'), (19, 21, '土'), (21, 23, '水')]

        for start, end, wuxing in ranges:
            if start <= shichen < end:
                return wuxing
        return '水'

    def get_dizhi_yinyang(self, shichen):
        """根据时辰获取地支阴阳"""
        ranges = [(1, 3, '阴'), (3, 5, '阳'), (5, 7, '阴'), (7, 9, '阳'),
                  (9, 11, '阴'), (11, 13, '阳'), (13, 15, '阴'), (15, 17, '阳'),
                  (17, 19, '阴'), (19, 21, '阳'), (21, 23, '阴')]

        for start, end, yinyang in ranges:
            if start <= shichen < end:
                return yinyang
        return '阳'

    def get_bagua(self, x, y, z):
        """根据三爻阴阳获取八卦"""
        key = (x, y, z)
        return self.bg_map.get(key, '')

    def sixgod(self, x):
        """根据数字获取六神"""
        return self.num_str[(x - 1) % 6]

    def get_changsheng(self, wuxing, dizhi):
        """获取长生十二宫状态"""
        dizhi_index = list(self.dizhi_number.keys()).index(dizhi)
        if wuxing in self.cs_dict:
            return self.cs_dict[wuxing][dizhi_index]
        return ''

    def get_wuxing_num(self, wuxing):
        """获取五行对应的数字"""
        return {'水': 1, '木': 2, '火': 3, '土': 4, '金': 5}.get(wuxing, 0)

    def get_sheng_ke_relation(self, ti, yong, ti_yinyang, yong_yinyang):
        """获取五行生克关系"""
        ti_num = self.get_wuxing_num(ti)
        yong_num = self.get_wuxing_num(yong)

        diff = abs(ti_num) - abs(yong_num)
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
            if ti_yinyang == yong_yinyang:
                return 5
            else:
                return 6

    def get_ti_yong_relation(self, ti_wuxing, shichen_wuxing, ti_yinyang, shichen_yinyang):
        """获取体用关系"""
        relation = self.get_sheng_ke_relation(ti_wuxing, shichen_wuxing, ti_yinyang, shichen_yinyang)
        relations = {
            1: '----用生体----',
            -1: '----体生用----',
            2: '----用克体----',
            -2: '----体克用----',
            3: '----体克用----',
            -3: '----用克体----',
            4: '----体生用----',
            -4: '----用生体----',
            5: '---体用比助---',  # 劫
            6: '---体用比助---'  # 助
        }
        if relation in [1, -1, 2, -2, 3, -3, 4, -4, 5, 6]:
            return relations[relation]
        else:
            return '---体用比劫---'

    def check_mu(self, liushen, time_dz):
        """检查是否入墓"""
        if liushen == '大安' and time_dz == '未':
            return '---入墓---'
        elif liushen == '速喜' and time_dz == '戌':
            return '---入墓---'
        elif liushen == '赤口' and time_dz == '丑':
            return '---入墓---'
        elif liushen in ['小吉', '空亡', '留连'] and time_dz == '辰':
            return '---入墓---'
        return '\t'

    def get_nongli_date(self):
        """获取当前农历日期"""
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        year = int(create_time[0:4])
        mouth = int(create_time[5:7])
        day = int(create_time[8:10])
        hourtime = int(create_time[11:13])
        mintime = int(create_time[14:16])

        if 24 > hourtime >= 23:
            hourtime = 00
            day += 1

        xin = datetime(year, mouth, day)
        return str(ZhDate.from_datetime(xin))

    def get_shichen_num(self, time_dz):
        """获取时辰对应的数字"""
        return self.dizhi_number.get(time_dz, 1)

    def calculate_liushen(self, numbers):
        """根据数字计算六神"""
        result = []
        temp = 0
        for id, i in enumerate(numbers):
            start = (i - 1) % 6
            process = (temp + start)
            # if id == 0:
            #     result.append(self.num_str[start])
            #     temp = start
            if process > 5:
                result.append(self.num_str[process % 6])
                temp = process % 6
            else:
                result.append(self.num_str[process])
                temp = process
        return result

    def calculate_wuxing(self, liushen_list):
        """根据六神计算五行"""
        result = []
        for liushen in liushen_list:
            result.append(self.six_five_map.get(liushen, '土'))
        return result

    def is_zodiac_character(self, char, choice=False, extract=False):
        """判断是否为地支字符"""
        zodiac_characters = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        if extract:
            return "".join([element for element in zodiac_characters if element in char])
        if not choice:
            return char in zodiac_characters
        elif choice:
            return any(element in char for element in zodiac_characters)

    def xlr(self, msg: str):
        """主函数：执行小六壬计算"""
        msg_list = msg.split(' ')

        # 例如：/小六壬 [问题] [选项(数字)] [数字(英文逗号)] [时辰(单字)] [详细/简短(default 0 or 1)]
        # 选项：1=时辰，2=随机数字，3=自定义数字
        # 例如：/小六壬 财运 1
        # 例如：/小六壬 财运 2
        # 例如：/小六壬 财运 3 1,2,3

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
            except Exception as e:
                return f"起课数字输入错误，请规范输入：{e}"

        # 处理时辰
        time_dz = '子'  # 默认值
        hour = int(time.strftime('%H', time.localtime(time.time())))
        if len(msg_list) == 5 or self.is_zodiac_character(msg, True):
            try:
                extracted_dz = self.is_zodiac_character(msg, extract=True)
                if self.is_zodiac_character(extracted_dz):
                    time_dz = extracted_dz
                    # 根据地支计算小时
                    ni_map = {'子': 23, '丑': 1, '寅': 3, '卯': 5, '辰': 7, '巳': 9,
                              '午': 11, '未': 13, '申': 15, '酉': 17, '戌': 19, '亥': 21}
                    hour = ni_map.get(time_dz, 23)
                elif choice == 3:
                    time_dz = self.get_dizhi(hour)
                else:
                    return "时辰不规范（请按照子，丑，寅等单字输入）"
            except Exception as f:
                return f

        # 判断输出详细程度
        c = 0 if "简短" in msg_list else 1

        # 根据选择方式生成数字
        list1 = []
        if choice == 1:
            # 随机抽取
            num_1 = random.randint(1, 6)
            num_2 = random.randint(1, 6)
            num_3 = random.randint(1, 6)
            list1 = [num_1, num_2, num_3]

        elif choice == 2:
            # 时间定数
            if self.is_zodiac_character(msg, True):
                return "时辰起课不能换时辰，请删除时辰后再试"

            nong = self.get_nongli_date()
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

            # 时辰数字
            num_3 = self.hourlist.index(time_dz) + 1
            list1 = [num_1, num_2, num_3]

        elif choice == 3:
            # 自行输入
            if len(number_list) != 3:
                return "数字请用英文逗号隔开，并且只容许三位，检查输入规范"
            list1 = number_list.copy()

        # 报数
        num_all = f"{list1[0]}, {list1[1]}, {list1[2]}"

        # 计算六神
        list2 = self.calculate_liushen(list1)
        x1, x2, x3 = list2[0], list2[1], list2[2]

        # 计算五行
        list3 = self.calculate_wuxing(list2)
        y1, y2, y3 = list3[0], list3[1], list3[2]

        # 当前时间信息
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        nong = self.get_nongli_date()
        dizhi_wx = self.get_dizhi_wuxing(hour)
        dizhi_sx = self.get_dizhi_yinyang(hour)
        sc_num = self.get_shichen_num(time_dz)

        # 输出结果
        if c == 0:
            text = f"""{create_time}
{nong}
问题：{problem}
报数：{num_all}
时辰：{time_dz}
{x1}  {x2}  {x3}
{y1}----{y2}----{y3}
{self.get_ti_yong_relation(y3, dizhi_wx, self.ls_yy_map.get(x3, ''), dizhi_sx)}
{self.check_mu(x3, time_dz)}

            """
            texts = [text]
        else:
            # 详细模式，这里简化处理，实际应该实现完整的排盘逻辑
            x1_1 = self.ls_yy_map.get(x1, '阳')
            x2_1 = self.ls_yy_map.get(x2, '阳')
            x3_1 = self.ls_yy_map.get(x3, '阳')

            # 简化的六神阴阳计算
            hls_x1 = self.hls[(self.get_shichen_num(time_dz) + 0 - 1) % 6]
            hls_x2 = self.hls[(self.get_shichen_num(time_dz) + 1 - 1) % 6]
            hls_x3 = self.hls[(self.get_shichen_num(time_dz) + 2 - 1) % 6]

            y1_1 = self.hls_yy_map.get(hls_x1, '阳')
            y2_1 = self.hls_yy_map.get(hls_x2, '阳')
            y3_1 = self.hls_yy_map.get(hls_x3, '阳')

            text1 = f"""{create_time}
{nong}
问题：{problem}
报数：{num_all}
时辰：{time_dz}
时辰五行：{dizhi_wx}
时辰阴阳：{dizhi_sx}
时辰排序：{sc_num}
{x1}  {x2}  {x3}
{y1}----{y2}----{y3}
{self.ls_yy_map.get(x1, '')}----{self.ls_yy_map.get(x2, '')}----{self.ls_yy_map.get(x3, '')}
{self.get_changsheng(y1, time_dz)}----{self.get_changsheng(y2, time_dz)}----{self.get_changsheng(y3, time_dz)}
{hls_x1}--{hls_x2}--{hls_x3}
{self.hls_yy_map.get(hls_x1, '')}----{self.hls_yy_map.get(hls_x2, '')}----{self.hls_yy_map.get(hls_x3, '')}
{self.get_ti_yong_relation(y3, dizhi_wx, self.ls_yy_map.get(x3, ''), dizhi_sx)}
{self.check_mu(x3, time_dz)}
"""
            text2 = f"""
*****穿八卦*****
本卦：{self.get_bagua(x1_1, x2_1, x3_1)}
类象：{self.bg_leixiang.get(self.get_bagua(x1_1, x2_1, x3_1), '')}
属性：{self.bg_wuxing.get(self.get_bagua(x1_1, x2_1, x3_1), '')}

客卦：{self.get_bagua(y1_1, y2_1, y3_1)}
类象：{self.bg_leixiang.get(self.get_bagua(y1_1, y2_1, y3_1), '')}
属性：{self.bg_wuxing.get(self.get_bagua(y1_1, y2_1, y3_1), '')}
***************
本卦在下，客卦在上
"""
            text3 = f"""
-----本卦-----
{self.bagua(self.get_bagua(x1_1, x2_1, x3_1))}
"""
            text4 = f"""
-----客卦-----
{self.bagua(self.get_bagua(y1_1, y2_1, y3_1))}
"""
            texts = [text1, text2, text3, text4]
        return texts

    def seach_bagua(self, msg: str):
        return [self.bagua(msg)]

# 创建全局实例
_xlr_instance = XiaoLiuRen()

def xlr(msg: str):
    """对外接口函数"""
    return _xlr_instance.xlr(msg)

if __name__ == '__main__':
    # /小六壬 [问题][选项(数字)][数字(英文逗号)][时辰(单字)][详细 / 简短(default 0 or 1)]
    a = xlr('/小六壬 财运 3 9,7,6 戌')
    print(a)
