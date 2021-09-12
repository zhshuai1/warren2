import dateutil

from strategy.stock_status import StockStatus
from validator.summary import Summary


class History:
    def __init__(self, code, trading_type, date, price, profit=0, reason=None):
        self.code = code
        self.trading_type = trading_type
        self.date = date
        self.price = price
        self.profit = profit
        self.reason = reason


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
