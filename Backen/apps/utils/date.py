import datetime


class DateRange():
    one_day = datetime.timedelta(days=1)
    one_week = datetime.timedelta(days=7)
    one_month = datetime.timedelta(days=30)
    """
    通用组
    """
    @classmethod
    def getToday(cls):
        """
        :return: 当前日期，格式为datetime
        """
        return datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    @classmethod
    def days(cls,n):
        #n可以是负数
        return (cls.getToday(), cls.getToday() + datetime.timedelta(days=n))
    @classmethod
    def hours(cls,n):
        return (cls.getToday(), cls.getToday() + datetime.timedelta(hours=n))
    """
    this组
    """
    @classmethod
    def this_day(cls):
        """
        :return: 返回一个(当天日期,下一天日期)的元组
        """
        return (cls.getToday(), cls.getToday() + cls.one_day)
    @classmethod
    def this_week(cls):
        today = cls.getToday()
        monday = today - datetime.timedelta(days = today.weekday())
        return (monday,monday+cls.one_week)
    @classmethod
    def this_month(cls):
        """
        :return: 返回本月1号到下个月1号的元组
        """
        today = cls.getToday()
        next_month = datetime.datetime(today.year + (today.month == 12),
                                       today.month == 12 or today.month + 1, 1, 0, 0, 0)
        return (today.replace(day=1), next_month)
    """
    next组
    1,7,30为了更快调用
    """
    @classmethod
    def next_day(cls):
        next = cls.getToday()+cls.one_day
        return (next, next + cls.one_day)
    @classmethod
    def next_7days(cls):
        return (cls.getToday(), cls.getToday() + cls.one_week)
    @classmethod
    def next_30days(cls):
        return (cls.getToday(),cls.getToday()+cls.one_month)
    """
    last组
    """
    @classmethod
    def last_day(cls):
        last = cls.getToday()-cls.one_day
        return (last, last + cls.one_day)
    @classmethod
    def last_7days(cls):
        return (cls.getToday(), cls.getToday() - cls.one_week)
    @classmethod
    def last_30days(cls):
        return (cls.getToday(),cls.getToday() - cls.one_month)