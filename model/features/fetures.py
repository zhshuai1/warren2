import datetime


class DayData:
    """

    """

    def __init__(self, date=datetime.date.today(), high=0, low=0, open=0, close=0, volume=0,
                 week=datetime.date.weekday(0)):
        self.date = date
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.volume = volume
        self.week = week


class Features:
    def __init__(self, code, industry):
        """
            `code` will be transformed to onehot, and since the code is sparse, the code will be compact to a
            smaller space by a mapping.
        """
        self.code = code
        self.industry = industry
        self.day = {"name": "day", "type": "array", "feature_type": "onehot"}
        self.minute = {"name": "minute", "type": "array", "feature_type": "onehot"}
        self.day_data = {"name": "day_data", "type": "array", "length": "20", "element_type": self.day}
        self.minute_data = {"name": "minute_data", "type": "array", "length": "20", "element_type": self.minute}

    def to_normalized_features(self):
        """
        :return: one vector that represents the normalized features. For some labels the method will transform them to onehot
        """
