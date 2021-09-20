import numpy as np
import tensorflow as tf


def test_tf1():
    a = tf.Variable(shape=(2, 1), initial_value=tf.random.normal(shape=(2, 1)))

    b = tf.constant(shape=(2, 1), value=[[.1], [.2]])
    print(f'***a is: ***\n{a}', )
    print(f'***b is: ***\n{b}', )

    with tf.GradientTape() as tape:
        tape.watch(a)
        tmp = a
        a.assign(b)
        print(f'***a is: ***\n{a}', )
        gradient = tape.gradient(a, a)
        print(f'***gradient is: ***\n{gradient}')


def test_tf2():
    a = tf.random.normal(shape=(2, 2))
    b = tf.random.normal(shape=(2, 2))

    with tf.GradientTape() as tape:
        tape.watch(a)  # Start recording the history of operations applied to `a`
        # c = tf.sqrt(tf.square(a) + tf.square(b))  # Do some math using `a`
        c = tf.square(a)
        # What's the gradient of `c` with respect to `a`?
        dc_da = tape.gradient(c, a)
        print(a)
        print(dc_da)


def test_tf3():
    a = tf.constant([[1, 2]])

    b = tf.constant([[1, -1]])
    print(a)
    print(b)
    c = tf.multiply(a, b)
    print(c.map_fn())


def test_tf4():
    y_true = [[1, 0], [0, 1], [0, 1], [1, 0]]
    y_pred = [[0.55, 0.45], [0.45, 0.55], [0.45, 0.55], [0.55, 0.45]]
    #y_pred = [[0.9993, 0.0007], [0.3144, 0.6856], [0.3144, 0.6856], [0.3144, 0.6856]]
    loss = tf.keras.losses.categorical_crossentropy(y_true, y_pred)
    l: object = loss.numpy()
    print(l)
    print(np.mean(l))


if __name__ == '__main__':
    test_tf4()
