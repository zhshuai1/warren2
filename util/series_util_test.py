import unittest

from strategy.stock_status import StockStatus
from util.series_util import highest, lowest, max_rise, max_fall, increase, minute_to_index, index_to_minute


class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.nums = [3, 2, 1, 4, 7, 1]
        self.nums2 = [3]
        self.nums3 = [9, 8, 7, 6, 5]
        self.nums4 = [3, 2, 1, 4, 7, 2]
        self.nums5 = [8, 9]

    def test_highest(self):
        self.assertEqual(7, highest(self.nums))
        self.assertEqual(3, highest(self.nums2))

    def test_lowest(self):
        self.assertEqual(0, lowest(self.nums))
        self.assertEqual(3, lowest(self.nums2))

    def test_max_rise(self):
        self.assertEqual(6, max_rise(self.nums))
        self.assertEqual(0, max_rise(self.nums2))
        self.assertEqual(0, max_rise(self.nums3))
        self.assertEqual(6, max_rise(self.nums4))

    def test_max_fall(self):
        self.assertEqual(1-1/7, max_fall(self.nums))
        self.assertEqual(0, max_fall(self.nums2))
        self.assertEqual(4/9, max_fall(self.nums3))
        self.assertEqual(1-2/7, max_fall(self.nums4))
        self.assertEqual(0, max_fall(self.nums5))

    def test_increase(self):
        self.assertEqual(-1, increase(self.nums))
        self.assertEqual(0, increase(self.nums2))
        self.assertEqual(5 / 9 - 1, increase(self.nums3))
        self.assertEqual(0.125, increase(self.nums5))

    def test_minute_to_index(self):
        self.assertEqual(0, minute_to_index(8, 0))
        self.assertEqual(1, minute_to_index(9, 30))
        self.assertEqual(5, minute_to_index(9, 34))
        self.assertEqual(80, minute_to_index(10, 49))
        self.assertEqual(121, minute_to_index(11, 30))
        self.assertEqual(121, minute_to_index(11, 45))
        self.assertEqual(121, minute_to_index(12, 15))
        self.assertEqual(122, minute_to_index(13, 0))
        self.assertEqual(135, minute_to_index(13, 13))
        self.assertEqual(242, minute_to_index(15, 0))
        self.assertEqual(242, minute_to_index(15, 10))

    def test_index_to_minute(self):
        self.assertEqual(index_to_minute(0), (8, 0))
        self.assertEqual(index_to_minute(1), (9, 30))
        self.assertEqual(index_to_minute(5), (9, 34))
        self.assertEqual(index_to_minute(80), (10, 49))
        self.assertEqual(index_to_minute(121), (11, 30))
        self.assertEqual(index_to_minute(122), (13, 0))
        self.assertEqual(index_to_minute(135), (13, 13))
        self.assertEqual(index_to_minute(242), (15, 0))


class TestMain2(unittest.TestCase):

    def test_aloha(self):
        a = 9
        print(f"{a} is 5.")
        print("%(name)d" % {"name": 9})
        print(f"{StockStatus.FREE.value}")
