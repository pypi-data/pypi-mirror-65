import re
from datetime import datetime

'''
    时间处理模块
'''


def get_time(data=None):
    '''
        获取数据时间
    :param  data 带时间参数的数据,如果为空获取当前时间
    :return:以%m-%d %H:%M:%S.%f格式返回时间
    '''
    time_format = "%m-%d %H:%M:%S.%f"
    if data is None:
        date = datetime.now().strftime(time_format)
    else:
        date = data
    t = re.search(r'{}'.format(r'(\d+)-(\d+) (\d+):(\d+):(\d+).(\d+)'), date)
    end_time = "{}-{} {}:{}:{}.{}".format(t.group(1), t.group(2), t.group(3), t.group(4), t.group(5),
                                          t.group(6)[:-3])
    return end_time


def count_time(init_time_data, end_time_data, year=False):
    '''
        结束数据-开始时间
    :param init_time_data:包含开始时间的数据
    :param end_time_data:包含结束时间的数据
    :return:相减后多少秒
    '''
    time1 = re.search(r'{}'.format(r'(\d+)-(\d+) (\d+):(\d+):(\d+).(\d+)'), init_time_data)  # 获取查找到数据
    time2 = re.search(r'{}'.format(r'(\d+)-(\d+) (\d+):(\d+):(\d+).(\d+)'), end_time_data)  # 获取查找到数据
    print(end_time_data)
    time1s = int(time1.group(3)) * 60 * 60 + int(time1.group(4)) * 60 + int(time1.group(5)) + int(time1.group(3))
    time2s = int(time2.group(3)) * 60 * 60 + int(time2.group(4)) * 60 + int(time2.group(5)) + int(time2.group(3))
    startDay = '{}-{}-{}'.format(str(datetime.now().year), str(time1.group(1)), str(time1.group(2)))
    endDay = '{}-{}-{}'.format(str(datetime.now().year), str(time2.group(1)), str(time2.group(2)))
    if int(time2.group(1)) < int(time1.group(1)) and year:
        startDay = '{}-{}-{}'.format(str(datetime.now().year - 1), str(time1.group(1)), str(time1.group(2)))
    days = (datetime.strptime(endDay, "%Y-%m-%d") - datetime.strptime(startDay, "%Y-%m-%d")).days
    # print(days)
    return "%.3f" % (days * 24 * 60 * 60 + time2s - time1s)


# def year_count_day(year):
#     '''
#         统计当前年有多少天
#     :param year:输入年
#     :return:有多少天
#     '''
#     startDay = str(year) + '-01-01'  # 一年第一天
#     endDay = str(year) + '-12-31'  # 一年最后一天
#
#     # 天数
#     year_days_mum = (datetime.datetime.strptime(endDay, "%Y-%m-%d") - datetime.datetime.strptime(startDay,
#                                                                                                  "%Y-%m-%d")).days + 1
#     return year_days_mum
#
#
# def month_count_day(year, month):
#     '''
#         统计当前月有多少天
#     :param year:输入年
#     :param month:输入月
#     :return:有多少天
#     '''
#     return calendar.monthrange(year, int(month))[1]


if __name__ == '__main__':
    print(get_time())
    # print(count_time("01-01 11:45:09.175  dd dd", "01-01 11:45:9.176  dd dd"))
