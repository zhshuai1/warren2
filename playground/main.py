import datetime
import json

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# matplotlib.use('Qt5Agg')
# matplotlib.use('TkAgg')
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print(f"My name is {self.name} and age is {self.age}")


def test_plot():
    x = np.linspace(-10, 10, 1000)
    y1 = np.sin(x) * np.exp(x / 5)
    y2 = 1 / (1 + np.exp(-x))
    fig, ax = plt.subplots(1, 1)
    ax2 = ax.twinx()
    ax.plot(x, y1, 'g-')
    ax2.plot(x, y2, 'r-.')
    plt.show()


def test_animal():
    cls = Animal
    animal = cls("Dog", 9)
    animal.date = datetime.datetime(1900, 1, 1)
    animal.speak()
    print(animal.__dict__)


def test_sort():
    mm = [(f"{i}", (i - 2) ** 2) for i in [2, 1, 4, 3]]
    mm.sort()
    print(mm)


def test_simple():
    print(f"{int(True)} and {int(False)}")


if __name__ == '__main__':
    test_simple()
