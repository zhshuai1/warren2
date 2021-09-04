from enum import Enum


class StockStatus(Enum):
    FREE = 1
    BOUGHT = 2


class TradingType(Enum):
    BUY = 1
    SELL = 2
