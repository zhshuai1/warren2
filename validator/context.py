import dateutil

from strategy.stock_status import StockStatus
from validator.summary import Summary


class History:
    def __init__(self, code, trading_type, date, price):
        self.code = code
        self.trading_type = trading_type
        self.date = date
        self.price = price
        self.profit = 0


class Context:
    """
    record the status and history for a single code and strategy pair.
    """

    def __init__(self, code, strategy):
        self.code = code
        self.strategy = strategy
        self.status = StockStatus.FREE
        self.history = []

    def generate_summary(self):
        return Summary(self.code, self.history)
