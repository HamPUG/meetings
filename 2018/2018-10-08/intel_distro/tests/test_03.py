import random
import math

def test():
    L = [math.exp(random.random()+0.00001) for i in range(100)]

if __name__ == '__main__':
    import timeit
    print("exp of 100 random numbers")
    print(timeit.timeit("test()", setup="from __main__ import test"))

