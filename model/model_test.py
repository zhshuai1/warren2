from model.categorical_model import to_category
from unittest import TestCase
import keras.utils.np_utils


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
        self.assertFalse((to_category(0.031)-[1 if i == 12 else 0 for i in range(19)]).any())
