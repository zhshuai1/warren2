from strategy.minute_check_strategy import MinuteCheckStrategy1
from strategy.stock_status import StockStatus
from strategy.stratety import Strategy
from util import series_util


class OnlyToday(Strategy):
    def __init__(self, stock):
        super(OnlyToday, self).__init__(stock, True, MinuteCheckStrategy1())

    def check_buy(self, index, context):
        return True

    def check_sell(self, index, context):
        if self.stock[index]['date'] > context.bought_date:
            context.status = StockStatus.FREE
        return self.status == StockStatus.FREE
