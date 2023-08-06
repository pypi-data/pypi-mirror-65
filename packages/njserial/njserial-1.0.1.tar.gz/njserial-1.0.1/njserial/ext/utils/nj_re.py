import re

'''
    正则匹配模块
    match : 从第一个字段开始匹配
    search：全局搜索匹配
    sub：替换数据
    split 分割字符串-返回列表
    findall：查找所有符合的数据-返回列表
    r' ' 表示原⽣字符串
    \d ：匹配数字，\D：匹配非数字
    \w ：匹配单字符串  \W：匹配⾮单词字符
    [4-7]：匹配括号中字符
    \：\\\\匹配
    ()：分组匹配-->r.group(1)
    + 出现1次或者⽆限次
    ? 出现1次或者0次--在最后一个值前加可关闭贪婪模式
    {m} 连续出现m次
    {m,} 前⼀个字符出现m次-->至少有多少个相连接
    {m,n} 出现从m到n次
    ^ 匹配字符串开头
    $ 匹配字符串结尾
    匹配. --> \.
    匹配中文 -->'[\u4e00-\u9fa5]'
'''


def rm_to_str(data, filter=' '):
    '''
       分割字符串返回字符串
    :param data:初始数据
    :param filter:分割条件(分割后去除)
    :return:分割后列表
    '''
    return re.sub(r"{}".format(filter), '', data)


def rm_to_list(data, filter=' '):
    '''
       分割字符串返回list
    :param data:初始数据
    :param filter:分割条件(分割后去除)
    :return:分割后列表
    '''
    return re.split(r"{}".format(filter), data)


def find_rm_match(data, filter='.+\.'):
    '''
        查找删除数据（从开头）--初始：提取毫秒时间
    :param data:初始数据
    :param filter:匹配条件
    :return:删除匹配条件后数据
    '''
    a = re.match(r'{}'.format(filter), data).group()  # 获取查找到数据
    return rm_to_str(data, a)


def find_rm_search(data, filter='.+\.'):
    '''
        查找删除数据（从中间匹配）
    :param data:初始数据
    :param filter:匹配条件
    :return:删除匹配条件后数据
    '''
    a = re.search(r'{}'.format(filter), data).group()  # 获取查找到数据
    return rm_to_str(data, a)


def find_rm_second(data, second=2, filter='.+? '):
    '''
        查找删除匹配格式出现次数数据
    :param data:初始数据
    :param second:第几次前删除
    :param filter:查找格式
    :return:删除后数据
    '''
    str1 = find_data_second(data, second, filter)
    return rm_to_str(data, str1)


def find_data_second(data, second=2, filter='.+? '):
    '''
        查找匹配格式出现次数数据
    :param data:初始数据
    :param second:截取出现次数前数据
    :param filter:过滤条件
    :return:查找到的数据
    '''
    list1 = re.findall(r'{}'.format(filter), data)  # 获取查找到数据
    str1 = ''
    for i in range(second):
        str1 += list1[i]
    return str1


def find_add_match(data, data1, filter='.+\.'):
    '''
        查找添加数据（从开头）
    :param data:初始数据
    :param data1:要添加的数据
    :param filter:过滤条件
    :return:添加后数据
    '''
    a = re.match(r'{}'.format(filter), data).group()  # 获取查找到数据
    return "{}{}".format(a, data1)


def find_add_search(data, data1, filter='.+\.'):
    '''
        查找添加数据（从中间匹配）
    :param data:初始数据
    :param data1:要添加的数据
    :param filter:过滤条件
    :return:添加后数据
    '''
    a = re.search(r'{}'.format(filter), data).group()  # 获取查找到数据
    return "{}{}".format(a, data1)


def find_data(data, filter):
    '''
        按格式截取数据
    :param data:初始数据
    :param filter:截取条件
    :return:截取到的数据
    '''
    return re.search(r'{}'.format(filter), data).group()


def find_mid_search(data, filter='{', filter1='}'):
    '''
        查找截取中间值
    :param data:初始数据
    :param filter:过滤初
    :param filter1:过滤尾
    :return:从过滤初到过滤尾查的数据
    '''
    r = re.search(r'({}.+{})'.format(filter, filter1), data)  # 获取查找到数据
    return r.group(1)
