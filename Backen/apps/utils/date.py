import datetime

one_day = datetime.timedelta(days=1)
one_week = datetime.timedelta(days=7)
one_month = datetime.timedelta(days=30)
def getToday():
    """
    :return: 当前日期，格式为datetime
    """
    return datetime.datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
def this_day():
    """
    :return: 返回一个(当天日期,下一天日期)的元组
    """
    return (getToday(),getToday()+one_day)

def this_week():
    today = getToday()
    monday = today - datetime.timedelta(days = today.weekday())
    return (monday,monday+one_week)

def next_7days():
    return (getToday(), getToday() + one_week)

def this_month():
    """
    :return: 返回本月1号到下个月1号的元组
    """
    today = getToday()
    next_month = datetime.datetime(today.year + (today.month == 12),
                                   today.month == 12 or today.month + 1, 1, 0, 0, 0)
    return (today.replace(day=1), next_month)

def next_30days():
    return (getToday(),getToday()+one_month)