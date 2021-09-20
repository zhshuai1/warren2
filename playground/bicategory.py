import random

import numpy as np
from keras.layers import Dense, Input
from keras.models import Model
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt
from keras.optimizer_v2.rmsprop import RMSprop
from keras.optimizer_v2.adam import Adam


def gen_data(x_range, y_range):
    return [((x, y), (int(x * y > 0), int(x > 0))) for x in x_range for y in y_range]


def test_bicategory():
    inputs = Input(shape=(2))
    x = Dense(2, activation='sigmoid')(inputs)
    x = Dense(2, activation='sigmoid')(x)
    y = Dense(2, activation='sigmoid')(x)
    model = Model(inputs=inputs, outputs=y)
    optimizer = Adam(learning_rate=0.01)
    optimizer = RMSprop(lr=0.01)
    model.compile(optimizer=optimizer, loss='binary_crossentropy',
                  metrics=['acc', 'binary_accuracy', 'categorical_accuracy', 'mse', 'AUC', 'Precision', 'Recall'])
    instances = gen_data(np.linspace(-2, 1, 100), np.linspace(-1, 1, 30))
    random.shuffle(instances)
    input = np.array(list(map(lambda x: x[0], instances)))
    output = np.array(list(map(lambda x: x[1], instances)))
    tensorboard = TensorBoard(log_dir='./logs')
    history = model.fit(input, output, batch_size=40, epochs=3000, callbacks=tensorboard)
    model.evaluate(input, output)
    res = model.predict(input)
    for i in range(len(input)):
        print(f"{input[i]}: {output[i]}: {[int(res[i][0] > 0.5), int(res[i][1] > 0.5)]}: {res[i]}")
    instances = gen_data(np.linspace(-1, 1, 23), np.linspace(-1, 1, 79))
    random.shuffle(instances)
    input = np.array(list(map(lambda x: x[0], instances)))
    output = np.array(list(map(lambda x: x[1], instances)))
    model.evaluate(input, output)
    res = model.predict(input)
    for i in range(30):
        print(f"{input[i]}: {output[i]}: {[int(res[i][0] > 0.5), int(res[i][1] > 0.5)]}: {res[i]}")


if __name__ == '__main__':
    test_bicategory()
