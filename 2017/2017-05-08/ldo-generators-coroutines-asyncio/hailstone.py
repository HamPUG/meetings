#+
# Example generator that yields a “hailstone sequence”
# <http://en.wikipedia.org/wiki/Collatz_conjecture>
#-

def hailstone(n) :
    assert isinstance(n, int) and n >= 1, "bad starting value"
    while True :
        yield n
        if n == 1 :
            break
        if n % 2 != 0 :
            n = 3 * n + 1
        else :
            n //= 2
        #end if
    #end while
#end hailstone
