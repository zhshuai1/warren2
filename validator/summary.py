import json

from strategy.stock_status import TradingType


class Summary:
    def __init__(self, code, history):
        self.code = code
        self.history = history
        self.trading_time = 0
        self.total_profit = 1
        self.avg_profit = 0
        self.max_profit = 0
        self.max_loss = 0
        for i in range(0, len(self.history) - 1, 2):
            if history[i].trading_type != TradingType.BUY or history[i + 1].trading_type != TradingType.SELL:
                print(f"stock {self.code} is abnormal.")
            self.trading_time += 1
            this_profit = history[i + 1].price / history[i].price
            history[i + 1].profit = this_profit - 1
            self.total_profit *= this_profit
            this_profit -= 1
            if this_profit > self.max_profit:
                self.max_profit = this_profit
            if this_profit < self.max_loss:
                self.max_loss = this_profit

            if not -0.1 <= this_profit <= 0.1:
                print(f"code: {history[i].code}, date: {history[i].date}, delta: {this_profit}")

    def __str__(self):
        return json.dumps(self.__dict__)
