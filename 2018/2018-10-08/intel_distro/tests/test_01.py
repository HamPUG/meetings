def test():
    # taken from:
    # https://docs.python.org/3.5/library/timeit.html
    L = [i for i in range(1000)]

if __name__ == '__main__':
    import timeit
    print("list with 1,000 elements")
    print(timeit.timeit("test()", setup="from __main__ import test"))

