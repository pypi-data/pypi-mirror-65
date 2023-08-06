import time

from interval import Interval


def get_week_day(day):
    week_day_dict = {
        1: '一',
        2: '二',
        3: '三',
        4: '四',
        5: '五',
        6: '六',
        0: '日',
    }
    return week_day_dict[day]


def date_str():
    return "{}  {}".format(time.strftime("%Y/%m/%d"), get_week_day(int(time.strftime("%w"))))


def is_stock_time():
    return time.strftime("%H:%M") in Interval("09:30", "15:00")


def is_screen_work_time():
    return time.strftime("%H:%M") in Interval("06:00", "24:00")
