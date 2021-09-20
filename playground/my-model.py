from functools import reduce

import keras.utils.np_utils
import numpy as np
from keras import backend
from keras.optimizer_v2.gradient_descent import SGD
from scipy.special import softmax
import matplotlib.pyplot as plt
from keras.layers import Input, Activation, Dense
from keras.models import Model
import keras
import keras.utils.vis_utils as vu
import tensorflow as tf
from keras.losses import CategoricalCrossentropy
from keras.optimizer_v2.adagrad import Adagrad
from keras.optimizer_v2.adadelta import Adadelta


def gen_data(fun, num):
    data = [[np.random.randint(0, 2), np.random.randint(0, 2)] for i in range(num)]
    label = list(map(fun, data))
    onehot = keras.utils.np_utils.to_categorical(label, 2)
    return np.array(data), np.array(onehot)


def loss_fn(y_true, y_pred):
    # print(f'***y_true: ***\n{y_true}')
    # print(f'***y_pred: ***\n{y_pred}')
    # loss = keras.losses.categorical_crossentropy(y_true, y_pred)
    # print(f'***loss: ***\n{loss}')
    # return loss
    squared_difference = tf.square(y_true - y_pred)
    return tf.reduce_mean(squared_difference, axis=-1)  # Note the `axis=-1`


def input_to_onehot(data):
    return np.array(list(map(lambda e: [e[0], 1 - e[0], e[1], 1 - e[1]], data)))


def extend_input(data):
    return np.array(list(map(lambda e: [e[0], e[1], e[0] & e[1]], data)))


def test_and():
    data, onehot = gen_data(lambda e: e[0] ^ e[1], 30)
    data = (data)
    inputs = Input(shape=(2,))
    activation = Activation('sigmoid')
    x = Dense(2, activation=activation)(inputs)
    y = Dense(2, activation='softmax')(x)
    model = Model(inputs=inputs, outputs=y)
    loss_fun = CategoricalCrossentropy(reduction='sum')
    # model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['acc'])

    model.compile(optimizer=Adagrad(learning_rate=0.05), loss=keras.losses.CategoricalCrossentropy(), metrics=['acc'])
    his = model.fit(data, onehot, batch_size=7, epochs=2000)
    model.evaluate(data, onehot)
    vu.plot_model(model, show_shapes=True, show_layer_names=True, show_dtype=True)
    print(model.predict(([[0, 0], [0, 1], [1, 0], [1, 1]])))

    plt.plot(his.history.get('acc'))
    plt.plot(his.history.get('loss'))
    plt.show()


def test_integrated_learning():
    pass


if __name__ == '__main__':
    test_and()
