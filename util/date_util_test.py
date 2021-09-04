import datetime
import unittest
from time import mktime

from util.date_util import from_timestamp, timestamp, from_year_month_day, make_time
from util.date_util import FORMAT


class TestMain(unittest.TestCase):
    def test_datetime_timestamp(self):
        dt = from_year_month_day(2021, 8, 29)
        ts = timestamp(dt)
        self.assertEqual(1630166400, ts)
        self.assertEqual(dt, from_timestamp(ts))
        print(f"{dt.strftime(FORMAT)}, and timestamp is {timestamp(dt)}")
        dt = dt.astimezone(datetime.timezone.utc)
        print(f"{dt.strftime(FORMAT)}, and timestamp is {timestamp(dt)}")

        str1 = "20210829-000001"
        dt = dt.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
        print(f"{dt.strftime(FORMAT)}, and timestamp is {timestamp(dt)}")
        dt = dt.strptime(str1, FORMAT)
        self.assertEqual(timestamp(dt), timestamp(make_time(str1, offset=8)))
        print(f"{timestamp(dt)},and tzname: {dt.tzname()}")
        tz = datetime.timezone(datetime.timedelta(hours=8))
        print(f"{tz.utcoffset(None).seconds}")
