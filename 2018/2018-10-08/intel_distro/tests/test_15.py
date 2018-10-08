import random
import numpy as np

def test():
    # taken from:
    # http://www.scipy-lectures.org/intro/numpy/operations.html
    a = np.array([1, 2, 3, 4])
    a + 1

if __name__ == '__main__':
    import timeit
    print("array + scalar")
    print(timeit.timeit("test()", setup="from __main__ import test"))

