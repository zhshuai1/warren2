import numpy as np
import matplotlib.pyplot as plt


def test_plot():
    x = [i for i in range(100)]
    s = [f"hello{i}" for i in range(100)]
    y = [np.sin(i / 10) for i in range(100)]
    ax = plt.gca()
    ax.set_xticks(x[::30])
    # plt.xticks(rotation=-90)
    # ax.tick_params(direction='out', length=10, width=1, colors='r',
    #                grid_color='r', grid_alpha=0.5)
    ax.set_title("Test alpha")
    plt.plot(x, np.sin(np.array(x)/9), label="xxx")
    plt.plot(x, np.sin(np.array(x)/10), label="xxx")
    # plt.plot(s, y, label="sss")

    ax.legend()
    plt.show()


if __name__ == '__main__':
    test_plot()
