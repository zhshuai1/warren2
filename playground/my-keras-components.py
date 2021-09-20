import math

import keras.metrics
import matplotlib.pyplot as plt
import numpy as np
from keras.metrics import Accuracy, BinaryAccuracy, CategoricalAccuracy, TopKCategoricalAccuracy, \
    MeanSquaredError, CategoricalCrossentropy, Hinge
from scipy.special import softmax
import tensorflow as tf
from keras.activations import relu, sigmoid, elu, selu, leaky_relu, tanh, softplus, softmax
from tensorflow.python.keras.optimizer_v2.adam import Adam
from tensorflow.python.ops.gen_math_ops import Sigmoid
from tensorflow.python.ops.gen_nn_ops import Relu


class MyMetrics(keras.metrics.Metric):

    def __init__(self):
        self.count = 0
        self.total = 0

    def update_state(self, *args, **kwargs):
        y_true = args[0]
        y_pred = args[1]
        for i in range(len(y_true)):
            self.total += 1
            if y_true[i] > y_pred[i]:
                self.count += 1

    def result(self):
        return self.count / self.total


def test_accuracy():
    acc = Accuracy()
    print(f"acc is: {acc.result()}")
    acc.update_state([3.1], [3.1])
    acc.update_state([3.1], [3.101])
    print(f"acc is: {acc.result().numpy()}, total: {acc.result()} and count: {acc}")


def test_binary_accuracy():
    acc = BinaryAccuracy(threshold=0.5)
    print(f"acc is: {acc.result()}")
    acc.update_state([[1, 1, 0, 0], [1, 6, -6, 0]], [[0.8, 0.7, 0.2, 0.3], [1, 1, 1, 1]], sample_weight=[1, 0])
    # acc.update_state([[1], [1], [0], [0]], [[0.98], [1], [0], [0.6]], sample_weight=[1, 0, 0, 1])
    print(f"acc is: {acc.result()}")


def test_topk_categorical_accuracy():
    acc = TopKCategoricalAccuracy(k=1)
    acc.update_state([[0, 1, 0], [1, 0, 0]], [[0.1, 0.8, 0.9], [0.1, 0, 0.9]])
    print(f"acc is: {acc.result()}")


def test_mse():
    acc = MeanSquaredError()
    acc.update_state([[1, 0, 0], [0, 1, 0]], [[0.9, 0.2, 0.1], [0.1, 0.8, 0.2]])
    print(f"acc is: {acc.result()}")
    print(f"{(0.01 + 0.04 + 0.01 + 0.01 + 0.04 + 0.04) / 6}")
    acc.update_state([0, 0, 1], [0.2, 0.1, 0.7])
    print(f"acc is: {acc.result()}")
    print(f"{(0.01 + 0.04 + 0.01 + 0.01 + 0.04 + 0.04 + 0.04 + 0.01 + 0.09) / 9}")


def test_categorical_crossentropy():
    acc = CategoricalCrossentropy(from_logits=False)
    acc.update_state([[1, 0, 0], [0, 1, 0]], [[0.9, 0.0, 0.1], [0.0, 0.8, 0.2]])
    print(f"acc is: {acc.result()}")
    print(f"{(-math.log(0.9) - math.log(0.8)) / 2}")
    acc.update_state([0, 0, 1], [0.2, 0.1, 0.7])
    print(f"acc is: {acc.result()}")
    print(f"{(-math.log(0.9) - math.log(0.8) - math.log(0.7)) / 3}")


def test_categorical_crossentropy_from_logits():
    acc = CategoricalCrossentropy(from_logits=True)
    y1 = softmax([0.9, 0.0, 0.1])
    y2 = softmax([0.0, 0.8, 0.2])
    y3 = softmax([0.2, 0.1, 0.7])
    print(f"y1: {y1}, y2: {y2}, y3: {y3}")
    acc.update_state([[1, 0, 0], [0, 1, 0]], [[0.9, 0.0, 0.1], [0.0, 0.8, 0.2]])
    print(f"acc is: {acc.result()}")
    print(f"{(-math.log(0.53882253) - math.log(0.50046528)) / 2}")
    acc.update_state([0, 0, 1], [0.2, 0.1, 0.7])
    print(f"acc is: {acc.result()}")
    print(f"{(-math.log(0.53882253) - math.log(0.50046528) - math.log(0.46396343)) / 3}")
    print(f"{tf.square([3, 4, 5])}")
    tf_data = tf.square([3, 4, 5])
    for a in tf_data:
        print(f"{a}, ", end="")


def test_hinge():
    acc = Hinge()
    acc.update_state([[0, 1], [0, 0]], [[0.6, 0.4], [0.4, 0.6]])
    print(f"acc is: {acc.result()}")


def test_np():
    print(f"{np.argmax([[10, 3, 5, 0.8], [2, 3, 4, 5]], axis=0)}")


def test_activations():
    x = np.linspace(-10, 10, 1000)
    y_relu = relu(x, alpha=0.01, threshold=0.0, max_value=2.5)
    y_sigmoid = sigmoid(x)
    y_tanh = tanh(x)
    y_softplus = softplus(x)
    y_elu = elu(x)

    plt.subplot(3, 3, 1)
    plt.plot(x, y_relu)
    plt.subplot(3, 3, 2)
    plt.plot(x, y_sigmoid)
    plt.subplot(3, 3, 3)
    plt.plot(x, y_tanh)
    plt.subplot(3, 3, 4)
    plt.plot(x, y_softplus)
    plt.subplot(3, 3, 5)
    plt.plot(x, y_elu)
    plt.show()


def test_sgd():
    opt = tf.keras.optimizers.SGD(learning_rate=0.1, momentum=0.)
    # opt = Adam(learning_rate=0.1)
    var = tf.Variable(1.0)
    val0 = var.value()
    loss = lambda: (var ** 2) / 2.0  # d(loss)/d(var1) = var1
    # First step is `- learning_rate * grad`
    for i in range(300):
        step_count1 = opt.minimize(loss, [var]).numpy()
        val1 = var.value()
        gd1 = (val0 - val1).numpy()
        val0 = val1
        print(f"step_count: {step_count1}, val1: {val1}, gd1: {gd1} ")
    # On later steps, step-size increases because of momentum
    step_count2 = opt.minimize(loss, [var]).numpy()
    val2 = var.value()
    gd2 = (val1 - val2).numpy()
    print(f"gd1: {gd1}, gd2: {gd2}")


if __name__ == '__main__':
    test_sgd()
