import numpy as np

def test():
    m1 = np.random.rand(20, 20)
    m2 = np.random.rand(20, 20)
    np.dot(m1, m2)

if __name__ == '__main__':
    import timeit
    print("dot product of two random matrices (20x20)")
    print(timeit.timeit("test()", setup="from __main__ import test"))

