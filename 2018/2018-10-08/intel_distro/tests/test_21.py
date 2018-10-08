import numpy as np
from scipy import linalg

def test():
    # taken from:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.inv.html
    a = np.array([[1., 2.], [3., 4.]])
    linalg.inv(a)

if __name__ == '__main__':
    import timeit
    print("inverse of matrix")
    print(timeit.timeit("test()", setup="from __main__ import test"))

