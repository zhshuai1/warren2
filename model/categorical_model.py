import numpy as np

from datasource.db.db import StockSource
from math import trunc

from keras.models import Model
from keras.utils.np_utils import to_categorical
from keras.layers import Dense, Input

from util import series_util


def to_category(delta):
    label = 0
    if delta > 0.09:
        label = 9
    elif delta > -0.09:
        label = trunc(delta * 100)
    else:
        label = -9
    label += 9
    return to_categorical([label], 19)[0]


class CategoricalModel:
    def __init__(self, days):

        self.days = days
        # daily: open, close, high, low, 5d-avg, 10d-avg
        # total: delta, max_rise, max_fall, single_day_max, single_day_min
        label_size = 19
        input_dimension = self.days * 4 * label_size + 5
        inputs = Input(shape=(input_dimension,))
        x = Dense(days, activation='sigmoid')(inputs)
        x = Dense(days, activation='sigmoid')(x)
        output = Dense(label_size, activation='softmax')(x)
        self.model = Model(inputs=inputs, outputs=output)
        self.model.compile(optimizer='adagrad', loss='categorical_crossentropy', metrics=['acc'])

    def gen_day_data(self, day_data):
        open = day_data['open']
        close = day_data['close']
        high = day_data['high']
        low = day_data['low']
        delta = day_data['delta']
        sigma = delta + 1
        o = sigma * open / close - 1
        c = sigma - 1
        h = sigma * high / close - 1
        l = sigma * low / close - 1
        res = []
        res.extend(to_category(o))
        res.extend(to_category(c))
        res.extend(to_category(h))
        res.extend(to_category(l))
        return res

    def gen_training_data(self, stocks, f=None):
        instances = []
        stocks = list(filter(f, stocks)) if f else stocks
        for stock in stocks:
            if stock[0]['code'] in ['sh000001', 'sz399001', 'sz399006']:
                continue
            for i in range(len(stock) - self.days - 1, 0, -1):
                instance = []
                ss = stock[i + self.days:i:-1]
                authority = list(map(lambda s: s['authority'], ss))
                delta = list(map(lambda s: s['delta'], ss))
                # values = list(map(lambda v: v / values[0]) - 1, authority)
                max_rise = series_util.max_rise(authority)
                max_fall = series_util.max_fall(authority)
                single_day_max = max(delta)
                single_day_min = min(delta)
                diff = authority[-1] / authority[0] - 1
                statistics = [diff, max_rise, max_fall, single_day_max, single_day_min]
                for s in ss:
                    instance.extend(self.gen_day_data(s))
                instance.extend(statistics)
                stock_to_predict = stock[i - 1]
                high = stock_to_predict['high']
                close = stock_to_predict['close']
                target = (close + (high - close) * 0.5) / close * (1 + stock_to_predict['delta']) - 1
                instances.append((instance, to_category(target), stock_to_predict['code'], stock_to_predict['date']))
        return instances

    def train_model(self):
        ss = StockSource()
        codes = ss.get_all_stocks()[:100]
        stocks = [ss.get_stock_by_code(code['code'], limit=200) for code in codes]
        instances = self.gen_training_data(stocks)
        inputs = np.array(list(map(lambda p: p[0], instances)))
        outputs = np.array(list(map(lambda p: p[1], instances)))
        for i in range(20):
            print(f'input {i}: {inputs[i]}, and output {i}: {outputs[i]}')
        self.model.fit(inputs, outputs, epochs=10000, batch_size=100)
        self.model.evaluate(inputs, outputs)


if __name__ == '__main__':
    model = CategoricalModel(20)
    model.train_model()
