import numpy as np

test = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [-1, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 2, 3, 4, 5, 6],
]


def get_test_map():
    return np.array(test)


__all__ = "get_test_map"
