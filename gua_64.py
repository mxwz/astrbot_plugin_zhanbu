import re

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



def Search_txt(x):
    with open('./64/%d.txt' % (dict1[x]), 'r', encoding='utf-8') as file:
        content = ''
        start = False  # 标志是否匹配到了"传统解卦"
        for line in file:
            if re.search(r'传统解卦', line):
                start = True  # 匹配到关键字后开始保存
            if start:
                content += line  # 拼接累计读取的行
            if re.search(r'决策', line):
                break  # 匹配到第二个关键字，跳出循环
    print(content)


def Search_line(x, y, end_line_num=None):
    with open('./64/%d.txt' % (dict1[x]), 'r', encoding='utf-8') as file:
        content = ''
        start = False  # 标志是否匹配到了"传统解卦"
        for line in file:
            if re.search(r'--%s--' % str(y), line):
                start = True  # 匹配到关键字后开始保存
            if start:
                content += line  # 拼接累计读取的行
            if re.search(r'--%s--' % str(y+1), line):
                break  # 匹配到第二个关键字，跳出循环
    print(content)


def Search_last(x):
    with open('./64/%d.txt' % (dict1[x]), 'r', encoding='utf-8') as file:
        content = ''
        start = False  # 标志是否匹配到了"传统解卦"
        for line in file:
            if re.search(r'--6--', line):
                start = True  # 匹配到关键字后开始保存
            if start:
                content += line  # 拼接累计读取的行
            if re.search(r'--7--', line):
                break  # 匹配到第二个关键字，跳出循环
    print(content)


def Main():
    while True:
        a = input('\n--------\n请输入需要查询的64卦全名，例如(乾为天)\n--------\n')
        Search_txt(a)
        b = int(input('\n--------\n请输入需要查询该卦象的第几爻？例如(需要查看动爻一，则输入：1)：\n--------\n'))
        if b == 6 and b == 12:
            Search_last(a)
        else:
            if b >= 7:
                b %= 6
            Search_line(a, b)



if __name__ == '__main__':
    Main()
