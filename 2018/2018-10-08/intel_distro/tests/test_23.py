import numpy as np
from scipy.linalg import lu

def test():
    # taken from:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.lu.html
    A = np.array([[2, 5, 8, 7], [5, 2, 2, 8], [7, 5, 6, 6], [5, 4, 4, 8]])
    p, l, u = lu(A)

if __name__ == '__main__':
    import timeit
    print("LU decomposition")
    print(timeit.timeit("test()", setup="from __main__ import test"))

