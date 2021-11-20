from datasource.db.db import StockSource
from model.categorical_model import to_category
from unittest import TestCase
import keras.utils.np_utils
from keras.layers import Input, Dense, LSTM, Conv1D, Conv2D, Concatenate
from keras.models import Model
from keras.losses import MeanSquaredError, CategoricalCrossentropy
from keras.optimizer_v2.rmsprop import RMSProp
from keras.callbacks import TensorBoard
from keras.initializers.initializers_v2 import Ones, Zeros
from keras.utils.vis_utils import plot_model
from keras.utils.np_utils import to_categorical
from util import series_util
import numpy.random as random

import numpy as np

days = 20
day_feature_num = 4
meta_feature_num = 5
label_num = 19


class TestMain(TestCase):
    def test_to_category(self):
        # a = [4, 5, 7, 8, -9,-5]
        a = [30, 4, '-7', 23, 24, 0]
        print(keras.utils.np_utils.to_categorical(a, 40))
        print(len(keras.utils.np_utils.to_categorical(a)[0]))
        print(to_category(-0.131))
        print(to_category(-0.072))
        print(to_category(-0.0051))
        print(to_category(0.0031))
        print(to_category(0.031))
        print(to_category(0.11))
        self.assertFalse((to_category(0.031) - [1 if i == 12 else 0 for i in range(19)]).any())

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
        res.extend([o, c, h, l])
        return res

    def gen_training_data(self, stocks, days=20, f=None):
        summaries = {}
        instances = []
        stocks = list(filter(f, stocks)) if f else stocks
        for stock in stocks:
            if stock[0]['code'] in ['sh000001', 'sz399001', 'sz399006']:
                continue
            for i in range(len(stock) - days - 1, 0, -1):
                x1 = []
                x2 = []
                ss = stock[i + days:i:-1]
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
                    x1.append(self.gen_day_data(s))
                x2.append(statistics)
                stock_to_predict = stock[i - 1]
                high = stock_to_predict['high']
                close = stock_to_predict['close']
                target = (close + (high - close) * 0.5) / close * (1 + stock_to_predict['delta']) - 1
                y = to_category(target)
                instances.append({
                    'x1': x1,
                    'x2': statistics,
                    'y': y,
                    'code': stock_to_predict['code'],
                    'date': stock_to_predict['date']
                })
                if np.argmax(y) not in summaries:
                    summaries[np.argmax(y)] = 0
                summaries[np.argmax(y)] += 1

        print(f"{summaries}")
        return instances

    def build_model(self):
        day_input = Input(shape=(days, day_feature_num))
        x1 = day_input
        x1 = Conv1D(16, 5)(x1)
        lstm = LSTM(128)
        x1 = lstm(x1)

        meta_input = Input(shape=(meta_feature_num,))
        x2 = Dense(16, activation='tanh')(meta_input)

        concat = Concatenate()([x1, x2])
        y = Dense(label_num * 8, activation='sigmoid')(concat)
        y = Dense(label_num * 8, activation='sigmoid')(y)
        y = Dense(label_num, activation='softmax')(y)
        model = Model(inputs=[day_input, meta_input], outputs=y)
        optimizer = RMSProp(learning_rate=0.01)
        loss = CategoricalCrossentropy()
        model.compile(optimizer=optimizer, loss=loss, metrics=['acc', 'AUC', 'mse'])
        model.summary()
        plot_model(model)
        return model

    def test_lstm_conv_model(self):
        # build model
        model = self.build_model()
        model.load_weights('lstm.model')
        # gen data

        ss = StockSource()
        all_codes = list(ss.get_all_stocks())
        random.shuffle(all_codes)
        codes = all_codes[:500]
        stocks = [ss.get_stock_by_code(code['code'], limit=200) for code in codes]
        instances = self.gen_training_data(stocks, days)
        random.shuffle(instances)

        x1 = np.array(list(map(lambda e: e['x1'], instances)))
        x2 = np.array(list(map(lambda e: e['x2'], instances)))
        y = np.array(list(map(lambda e: e['y'], instances)))

        # train & validate
        model.fit([x1, x2], y, epochs=1000, batch_size=1000, callbacks=[TensorBoard()])
        model.evaluate([x1, x2], y)
        model.save('lstm.model')
        num = len(y)
        for _ in range(10):
            instance = instances[np.random.randint(0, num)]
            y_pred = model.predict([np.array([instance['x1']]), np.array([instance['x2']])])[0]
            print(f"code: {instance['code']}, date: {instance['date']}, y: {np.argmax(instance['y'])}\n"
                  f"p_label: {np.argmax(y_pred)}, y_pred: {y_pred}")

    def test_predict(self):
        model = self.build_model()
        model.load_weights('lstm.model')


def test_conv2d(self):
    conv2d = Conv2D(3, (2, 2), kernel_initializer=Ones(), bias_initializer=Zeros())
    data = np.arange(0., 120)
    data = data.reshape((1, 2, 3, 4, 5))
    y = conv2d(data)
    print(f"{data}")
    print(f"{y}")
    print(f"{y.shape}")


def test_conv1d(self):
    conv1d = Conv1D(3, 2, kernel_initializer=Ones(), bias_initializer=Zeros())
    data = np.arange(0., 120)
    data = data.reshape((1, 2, 3, 4, 5))
    y = conv1d(data)
    print(f"{data}")
    print(f"{y}")
    print(f"{y.shape}")
