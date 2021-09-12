from enum import Enum


class StockStatus(Enum):
    FREE = 1
    BOUGHT = 2


class TradingType(Enum):
    BUY = 1
    SELL = 2


class TradingReason(Enum):
    ENOUGH_GAIN = 1
    ENOUGH_LOSS = 2
    TIMEOUT = 3
