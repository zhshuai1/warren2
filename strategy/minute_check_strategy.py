import datetime
import json

from datasource.db.db import StockSource
from strategy.stock_status import StockStatus, TradingType, TradingReason
from strategy.stratety import Strategy
from util import series_util
from validator.context import History


# it's too hard for rule based strategy.
# I could not wait to switch to model based strategy.
class MinuteCheckStrategy1:
    """
    # simplest minute strategy:
    1. buy if min
    """

    def initialize(self, stock, time_range):
        self.stock_source = StockSource()

    def check_buy(self, stock, index, context):
        stock = stock[index]
        date = stock['date']
        minutes = self.stock_source.get_stock_minute_by_code_and_date(stock['code'], stock['date'])[0]['minute']
        if minutes is not None:
            minutes = json.loads(minutes)
            yesterday_close = minutes[0]['prevclose']
            today_open = minutes[1]['price']
            # check from 5th minute
            for i in range(6, len(minutes)):
                price = minutes[i]['price']
                if yesterday_close <= 0:
                    # print(f"code is {stock['code']} and yesterday close is {yesterday_close}")
                    return False
                if 1.005 <= price / yesterday_close <= 1.035:
                    context.code = stock['code']
                    context.status = StockStatus.BOUGHT
                    hour, minute = series_util.index_to_minute(i)
                    dt = datetime.datetime(date.year, date.month, date.day, hour, minute)
                    context.history.append(History(stock['code'], TradingType.BUY, dt, price))
                    return True
                # only buy in the morning
                if index > 100:
                    return False
        return False

    def check_sell(self, stock, index, context):
        stock = stock[index]
        if context.code != stock['code']:
            return False
        date: datetime.datetime = stock['date']
        minutes = self.stock_source.get_stock_minute_by_code_and_date(stock['code'], stock['date'])[0]['minute']
        if minutes is not None:
            minutes = json.loads(minutes)
            yesterday_close = minutes[0]['prevclose']
            if yesterday_close <= 0:
                print(f"code is {stock['code']}, date is {stock['date']}, and yesterday_close is {yesterday_close}")
                return False
            today_open = minutes[1]['price']
            hit = False
            reason = None
            for i in range(4, len(minutes)):
                price = minutes[i]['price']
                # enough profit
                if 1.005 <= price / yesterday_close:
                    hit = True
                    reason = TradingReason.ENOUGH_GAIN
                # too much loss
                if price < yesterday_close and price < today_open:
                    hit = True
                    reason = TradingReason.ENOUGH_LOSS

                # time constraint: should be sold in the morning
                if index >= 100:
                    hit = True
                    reason = TradingReason.TIMEOUT
                if hit:
                    context.status = StockStatus.FREE
                    hour, minute = series_util.index_to_minute(i)
                    dt = datetime.datetime(date.year, date.month, date.day, hour, minute)
                    context.history.append(History(stock['code'], TradingType.SELL, dt, price, reason=reason))
                    return True
        return False
