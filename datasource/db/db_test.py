from unittest import TestCase

from datasource.db.db import StockSource


class MainTest(TestCase):

    def test_get_stock_minute_by_code_and_date(self):
        ss = StockSource()
        s0 = ss.get_stock_by_code('sh600030', limit=1)
        dt = s0[0]['date']
        print(ss.get_stock_minute_by_code_and_date('sh600030', dt))
