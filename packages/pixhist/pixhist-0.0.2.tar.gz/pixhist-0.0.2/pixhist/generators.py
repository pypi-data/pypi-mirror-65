""" Examples of generator factories that can be used to make nice images.
"""
from numba import njit
import numpy as np


def clifford(a=-2.3, b=1.9, c=2.3, d=1.2, x_i=0, y_i=0):
    @njit
    def generator():
        x, y = x_i, y_i
        while True:
            yield x, y
            x_ = np.sin(a * y) + c * np.cos(a * x)
            y_ = np.sin(b * x) + d * np.cos(b * y)
            x, y = x_, y_
    return generator
