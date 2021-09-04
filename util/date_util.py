import datetime

FORMAT = "%Y%m%d-%H%M%S"

dt = datetime.datetime(1900, 1, 1)


def from_timestamp(ts, tzinfo=datetime.timezone(datetime.timedelta(hours=8))):
    """
    integer to datetime
    :param ts:
    :param tzinfo:
    :return:
    """
    return dt.fromtimestamp(ts, tz=tzinfo)


def timestamp(t):
    """
    datetime to integer
    :param t:
    :return:
    """
    return t.timestamp()


def format_time(t: datetime, offset=8):
    """
    datetime to string
    :param offset:
    :param t:
    :return:
    """
    t.astimezone(datetime.timezone(datetime.timedelta(hours=offset)))
    return t.strftime(FORMAT)


def make_time(s, offset=8):
    """
    string to integer
    :param offset:
    :param s:
    :return:
    """
    s += "+%02d00" % offset
    return dt.strptime(s, FORMAT + "%z")


def from_year_month_day(year, month, day, tzinfo=datetime.timezone(datetime.timedelta(hours=8))):
    """
    construct a date time with year, month and day, default timezone GMT+8
    :param year:
    :param month:
    :param day:
    :param tzinfo:
    :return:
    """
    return datetime.datetime(year, month, day, 0, 0, 0, tzinfo=tzinfo)
