import numpy as np

def test():
    # taken from:
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.gamma.html
    shape, scale = 2., 2.  # mean=4, std=2*sqrt(2)
    s = np.random.gamma(shape, scale, 1000)

if __name__ == '__main__':
    import timeit
    print("1000 gamma distributed random numbers")
    print(timeit.timeit("test()", setup="from __main__ import test"))

