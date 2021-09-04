from datasource.db.db import StockSource
from strategy.stratety import Strategy
from strategy.day_continuously_growing import DayContinuouslyGrowing
from strategy.minute_check_strategy import MinuteCheckStrategy1
from validator.context import Context


class Validator:
    def __init__(self, stocks, strategies, time_range):
        self.stocks = stocks
        self.strategies = strategies
        self.time_range = time_range
        self.summaries = []
        self.total_times = 0
        self.avg_profit = 0

    def validate(self):
        for strategy in self.strategies:
            for stock in self.stocks:
                code = stock[0]['code']
                context = Context(code, strategy)
                strategy.run(stock, self.time_range, context)
                summary = context.generate_summary()
                self.summaries.append(summary)

    def summary(self):
        """
            show summary
        :return: None
        """
        self.total_times = 0
        total_profit = 0
        for s in self.summaries:
            # if history num is an odd, only buy, will ignore it.
            if len(s.history) <= 1:
                continue
            self.total_times += s.trading_time & ~1
            total_profit += s.total_profit-1
        self.avg_profit = total_profit / self.total_times


if __name__ == '__main__':
    start = 1000
    step = 300
    source = StockSource()
    stock_codes = source.get_all_stocks()[start:start + step]
    print(f"codes are {stock_codes}")
    stocks = [source.get_stock_by_code(entry['code'], 400) for entry in stock_codes]
    strategy1 = Strategy(DayContinuouslyGrowing, MinuteCheckStrategy1)
    strategies = [strategy1]
    time_range = range(50, 0, -1)
    validator = Validator(stocks, strategies, time_range)
    validator.validate()
    validator.summary()
    print(
        f"avg_profit: {validator.avg_profit}, times: {validator.total_times}, "
        f"and detailed summary is {validator.summaries}")
    exit(0)
