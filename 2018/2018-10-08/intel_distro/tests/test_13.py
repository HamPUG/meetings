import numpy as np

def test():
    # taken from:
    # https://www.tutorialspoint.com/python/python_normal_distribution.htm
    s = np.random.normal(0.0, 1.0, 1000)

if __name__ == '__main__':
    import timeit
    print("1000 normal distributed random numbers")
    print(timeit.timeit("test()", setup="from __main__ import test"))

