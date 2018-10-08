import random

def test():
    L = [random.random() for i in range(100)]

if __name__ == '__main__':
    import timeit
    print("list of 100 random numbers")
    print(timeit.timeit("test()", setup="from __main__ import test"))

