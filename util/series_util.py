import math
from functools import reduce


def increase(series):
    return series[-1] / series[0] - 1


def max_rise(series):
    left_min = [series[0]]
    for i in range(1, len(series)):
        new_min = min(left_min[i - 1], series[i])
        left_min.append(new_min)
    res = 0
    for i in range(1, len(series)):
        res = max(res, series[i] / left_min[i] - 1)
    return res


def max_fall(series):
    left_max = [series[0]]
    for i in range(1, len(series)):
        new_max = max(left_max[i - 1], series[i])
        left_max.append(new_max)
    res = 0
    for i in range(1, len(series)):
        res = min(res, series[i] / left_max[i] - 1)
    return -res


def highest(series):
    # return reduce(lambda a, b: a if a > b else b, series)
    return max(series)


def lowest(series):
    # return reduce(lambda a, b: a if a < b else b, series)
    return min(series)


def minute_to_index(hour, minute):
    if hour >= 15:
        return 242
    elif hour >= 13:
        return (hour - 13) * 60 + minute + 122
    elif hour > 11 or (hour == 11 and minute > 30):
        return 121
    else:
        index = (hour - 9) * 60 + minute - 30 + 1
        if index > 0:
            return index
        else:
            # if index <=0; return the value of yesterday price
            return 0


def index_to_minute(index):
    if index == 0:
        return 8, 0
    elif index < 122:
        minute = index - 1 + 30
        return minute // 60 + 9, minute % 60
    else:
        minute = index - 122
        return minute // 60 + 13, minute % 60
