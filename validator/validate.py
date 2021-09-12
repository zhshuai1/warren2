from datasource.db.db import StockSource
from strategy.stock_status import TradingType, TradingReason
from strategy.stratety import Strategy
from strategy.day_continuously_growing import DayContinuouslyGrowing
from strategy.minute_check_strategy import MinuteCheckStrategy1
from util import date_util
from validator.context import Context

import matplotlib.pyplot as plt


class Indicators:
    def __init__(self, buy_times, sell_times, gain_times, loss_times, timeout_times,
                 this_profit, max_profit, min_profit, avg_profit):
        self.buy_times = buy_times
        self.sell_times = sell_times
        self.gain_times = gain_times
        self.loss_times = loss_times
        self.timeout_times = timeout_times
        self.this_profit = this_profit
        self.max_profit = max_profit
        self.min_profit = min_profit
        self.avg_profit = avg_profit


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
                strategy.simulate(stock, self.time_range, context)
                summary = context.generate_summary()
                self.summaries.append(summary)

    def simulate(self):
        for strategy in self.strategies:
            context = Context('code', strategy)
            strategy.simulate(self.stocks, self.time_range, context)
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
            total_profit += s.total_profit - 1
        self.avg_profit = total_profit / (self.total_times + 1e-10)

    def visualize(self):
        history_map = {}
        indicators_map = {}
        for s in self.summaries:
            for h in s.history:
                dt = date_util.format_time(h.date)
                if dt not in history_map:
                    history_map[dt] = []
                history_map[dt].append(h)
        for dt, hs in history_map.items():
            buy_times = 0
            sell_times = 0
            gain_times = 0
            loss_times = 0
            timeout_times = 0
            profit = 0
            this_profit = 0
            max_profit = 0
            min_profit = 0
            for h in hs:
                if h.trading_type == TradingType.BUY:
                    buy_times += 1
                if h.trading_type == TradingType.SELL:
                    sell_times += 1
                    this_profit = h.profit
                    profit += h.profit
                    if profit > max_profit:
                        max_profit = profit
                    if profit < min_profit:
                        min_profit = profit

                    if h.reason == TradingReason.ENOUGH_GAIN:
                        gain_times += 1
                    if h.reason == TradingReason.ENOUGH_LOSS:
                        loss_times += 1
                    if h.reason == TradingReason.TIMEOUT:
                        timeout_times += 1

            indicators_map[dt] = Indicators(buy_times, sell_times, gain_times, loss_times, timeout_times,
                                            this_profit, max_profit, min_profit, profit / (1e-10 + sell_times))

        indicators_list = list(indicators_map.items())
        indicators_list.sort()
        xxx = list(map(lambda e: e[0], indicators_list))
        plt.subplot(2, 1, 1)
        # plt.plot(xxx, list(map(lambda e: e[1].buy_times, indicators_list)), label='buy_times')
        # plt.plot(xxx, list(map(lambda e: e[1].sell_times, indicators_list)), label='sell_times')
        plt.plot(xxx, list(map(lambda e: e[1].gain_times, indicators_list)), label='gain_times')
        plt.plot(xxx, list(map(lambda e: e[1].loss_times, indicators_list)), label='loss_times')
        plt.plot(xxx, list(map(lambda e: e[1].timeout_times, indicators_list)), label='timeout_times')
        plt.legend()
        plt.xticks([])
        plt.subplot(2, 1, 2)
        profit_list = [1]
        for indicator in indicators_list:
            profit_list.append(profit_list[-1] * (indicator[1].this_profit + 1))

        plt.plot(xxx, list(map(lambda x: x - 1, profit_list[1:])), label='total_profit')
        # plt.plot(xxx, list(map(lambda e: e[1].max_profit, indicators_list)), label='max_profit')
        # plt.plot(xxx, list(map(lambda e: e[1].min_profit, indicators_list)), label='min_profit')
        plt.plot(xxx, list(map(lambda e: e[1].avg_profit, indicators_list)), label='avg_profit')
        ax = plt.gca()
        plt.legend()
        ax.set_xticks(list(range(0, len(xxx), 30)))
        plt.xticks(rotation=-90)
        plt.show()


if __name__ == '__main__':
    start = 000
    step = 4000
    source = StockSource()
    stock_codes = source.get_all_stocks()[start:start + step]
    print(f"codes are {stock_codes}")
    stocks = [source.get_stock_by_code(entry['code'], 200) for entry in stock_codes]
    strategy1 = Strategy(DayContinuouslyGrowing, MinuteCheckStrategy1)
    strategies = [strategy1]
    time_range = range(100, 0, -1)
    validator = Validator(stocks, strategies, time_range)
    validator.simulate()
    validator.summary()
    print(
        f"avg_profit: {validator.avg_profit}, times: {validator.total_times}, ")
    validator.visualize()
    exit(0)
