from strategy.minute_check_strategy import MinuteCheckStrategy1
from strategy.stock_status import StockStatus, TradingType
from strategy.stratety import Strategy
from util import series_util, date_util
from validator.context import History


class DayContinuouslyGrowing:
    def __init__(self):
        self.days = 21
        self.min_rise = 20
        self.max_fall = 10

    def check_buy(self, stock, index, context):
        if context.status == StockStatus.BOUGHT:
            return False
        if self.days + index >= len(stock):
            return False
        if stock[index+1]['code'] in ['sh000001', 'sz399001', 'sz399006']:
            return False
        # print(f"code: {stock[index + 1]['code']}, date:{stock[index + 1]['date']}, delta: {stock[index + 1]['delta']}")
        if not 0.005 <= stock[index + 1]['delta'] <= 0.035:
            return False
        values = list(map(lambda s: s['authority'], stock[index + 1:self.days + index]))
        values.reverse()
        if series_util.increase(values) > 0.2 and series_util.max_fall(values) < 0.1:
            return True
        return False

    def check_sell(self, stock, index, context):
        return context.status == StockStatus.BOUGHT and context.code == stock[0]['code']
        # bought_date = date_util.from_year_month_day(1900, 1, 1)
        # if len(context.history) > 0:
        #     last_record: History = context.history[-1]
        #     if last_record.trading_type == TradingType.BUY:
        #         bought_date = last_record.date
        #
        # if stock[index]['date'].timestamp() > bought_date.timestamp():
        #     context.status = StockStatus.FREE
        # return context.status == StockStatus.FREE
