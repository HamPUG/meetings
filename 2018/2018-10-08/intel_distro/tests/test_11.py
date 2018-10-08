import numpy as np

def test():
    np.random.rand(100, 100)

if __name__ == '__main__':
    import timeit
    print("random 100x100 matrix")
    print(timeit.timeit("test()", setup="from __main__ import test"))

