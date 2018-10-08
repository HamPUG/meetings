import numpy as np
from scipy.fftpack import fft, ifft

def test():
    # taken from:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.fft.html#scipy.fftpack.fft
    x = np.arange(5)
    np.allclose(fft(ifft(x)), x, atol=1e-15)

if __name__ == '__main__':
    import timeit
    print("fft and ifft")
    print(timeit.timeit("test()", setup="from __main__ import test"))

