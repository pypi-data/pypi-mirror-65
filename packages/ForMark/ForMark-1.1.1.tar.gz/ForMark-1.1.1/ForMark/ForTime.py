"""
时间处理
"""
import calendar
import time
import datetime

from ForMark.ForException import exception_return_decorator
from ForMark.ForString import is_none_str

# # 本周第一天和最后一天
# this_week_start = now - timedelta(days=now.weekday())
# this_week_end = now + timedelta(days=6 - now.weekday())
#
# # 上周第一天和最后一天
# last_week_start = now - timedelta(days=now.weekday() + 7)
# last_week_end = now - timedelta(days=now.weekday() + 1)
#
# # 本月第一天和最后一天
# this_month_start = datetime.datetime(now.year, now.month, 1)
# this_month_end = datetime.datetime(now.year, now.month + 1, 1) - timedelta(days=1)
#
# # 上月第一天和最后一天
# last_month_end = this_month_start - timedelta(days=1)
# last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
#
# # 本季第一天和最后一天
# month = (now.month - 1) - (now.month - 1) % 3 + 1
# this_quarter_start = datetime.datetime(now.year, month, 1)
# this_quarter_end = datetime.datetime(now.year, month + 3, 1) - timedelta(days=1)
#
# # 上季第一天和最后一天
# last_quarter_end = this_quarter_start - timedelta(days=1)
# last_quarter_start = datetime.datetime(last_quarter_end.year, last_quarter_end.month - 2, 1)
#
# # 本年第一天和最后一天
# this_year_start = datetime.datetime(now.year, 1, 1)
# this_year_end = datetime.datetime(now.year + 1, 1, 1) - timedelta(days=1)
#
# # 去年第一天和最后一天
# last_year_end = this_year_start - timedelta(days=1)
# last_year_start = datetime.datetime(last_year_end.year, 1, 1)

def get_this_week_range():
    """获取本周时间区间，返回时间对象

    方法1：
    today = datetime.datetime.now()
    oneday = datetime.timedelta(days=1)
    m1 = calendar.MONDAY
    while today.weekday() != m1:
        today -= oneday
    endday = today + datetime.timedelta(days=6)
    return datetime.datetime(today.year, today.month, today.day, 0, 0, 0), \
           datetime.datetime(endday.year, endday.month,
                             endday.day, 23, 59, 59)
    """
    return get_week_start(), get_week_end()


def get_week_start():
    # 获取本周开始时间
    now = datetime.datetime.now()
    this_week_start = now - datetime.timedelta(days=now.weekday())
    return datetime.datetime(this_week_start.year, this_week_start.month, this_week_start.day, 0, 0, 0)


def get_week_end():
    # 获取本周开始时间
    now = datetime.datetime.now()
    this_week_end = now + datetime.timedelta(days=6 - now.weekday())
    return datetime.datetime(this_week_end.year, this_week_end.month, this_week_end.day, 23, 59, 59)


def get_month_start():
    # 获取本月开始时间
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, 1, 0, 0, 0)


def get_month_end():
    # 获取本月结束时间
    now = datetime.datetime.now()
    year = now.year
    month = now.month + 1
    if month == 13:
        month = 1
        year += 1
    end = datetime.datetime(year, month, 1)-datetime.timedelta(days=1)
    return end



def get_this_week_range():
    """获取本周时间区间，返回时间对象"""
    today = datetime.datetime.now()
    oneday = datetime.timedelta(days=1)
    m1 = calendar.MONDAY
    while today.weekday() != m1:
        today -= oneday
    endday = today + datetime.timedelta(days=6)
    return datetime.datetime(today.year, today.month, today.day, 0, 0, 0), datetime.datetime(endday.year, endday.month,
                                                                                             endday.day, 23, 59, 59)


@exception_return_decorator(None)
def timestamp_to_time(timestamp) -> datetime.datetime:
    """
    时间戳转时间格式
    :param timestamp: 时间戳
    :return:
    """
    if is_none_str(timestamp):
        return None
    if isinstance(timestamp, datetime.datetime):
        return timestamp
    if isinstance(timestamp, str):
        timestamp = int(timestamp)
    if not isinstance(timestamp, int):
        return None
    if timestamp > 9999999999:
        timestamp = timestamp // 1000
    return datetime.datetime.fromtimestamp(timestamp)


def datetime_to_str(dt, format='%Y-%m-%d %H:%M'):
    if dt:
        return dt.strftime(format)
    else:
        return ''


def get_time_file():
    return time.strftime("%Y/%m/%d/")


if __name__ == '__main__':
    print(timestamp_to_time(1581902524433))
    print(type(timestamp_to_time(1581902524433)))
    print(type(timestamp_to_time(None)))
