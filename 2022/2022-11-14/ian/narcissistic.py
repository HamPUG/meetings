#/usr/bin/env python3
#
# narcissistic.py
#
# narcissistic number / Armstring number / pluperfect digital invariant (PPDI)
# plus perfect number (PPN)
#
# A number that is the sum of its own digits each raised to the power of the 
# number of digits. 
#
# E.g. 1³ + 5³ + 3³ = 153
# 1 + 125 + 27 = 153
#
# Ian Stewart 2022-10-28 ©CC0
#
import time
SUPER = ["⁰","¹","²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹",
         "¹⁰","¹¹","¹²", "¹³", "¹⁴", "¹⁵", "¹⁶", "¹⁷", "¹⁸", "¹⁹",
         "²⁰","²¹","²²", "²³", "²⁴", "²⁵", "²⁶", "²⁷", "²⁸", "²⁹",
         "³⁰","³¹","³²", "³³", "³⁴", "³⁵", "³⁶", "³⁷", "³⁸", "³⁹",      
]

count = 0
    
def find_narcissistic(i):
    global count
    i_str = str(i)    
    number_of_digits = len(i_str)
    #print(number_of_digits)
    total = 0
    for value in i_str:
        total += (int(value) ** number_of_digits)            
    if total == i:
        #print("narcissistic number:", str(i))
        count += 1
        s = ""
        t = ""
        for value in str(total):
            s += "{}{} + ".format(value, SUPER[number_of_digits])
            t += "{} + ".format(int(value) ** number_of_digits)
            
        s = s[:-2]        
        s += "= {}".format(i)
        
        t = t[:-2]        
        t += "= {}".format(i)
        
        print(count)      
        print(s)
        print(t) 
        print()
                       

if __name__=="__main__":
    start_time = time.time()
    #for i in range (0, 1000000): # 1M 2 secs 21
    for i in range (0, 10000000): # 10M 26 secs 25
    #for i in range (0, 100000000): # 100M 278 secs 28
    #for i in range (0, 1000000000): # 1B 3167 secs 32
    #for i in range (0, 115132219018763992565095597973971522402): 
        find_narcissistic(i)  

    end_time = time.time()
    print("Duration: {:.0f}s".format(end_time-start_time))    

"""
Reference:
https://en.wikipedia.org/wiki/Narcissistic_number



28
8⁸ + 8⁸ + 5⁸ + 9⁸ + 3⁸ + 4⁸ + 7⁸ + 7⁸ = 88593477
16777216 + 16777216 + 390625 + 43046721 + 6561 + 65536 + 5764801 + 5764801 = 88593477

Duration: 278s

ian@dell:~/Desktop/number$ python narcissistic.py
1
0¹ = 0
0 = 0

2
1¹ = 1
1 = 1

3
2¹ = 2
2 = 2

4
3¹ = 3
3 = 3

5
4¹ = 4
4 = 4

6
5¹ = 5
5 = 5

7
6¹ = 6
6 = 6

8
7¹ = 7
7 = 7

9
8¹ = 8
8 = 8

10
9¹ = 9
9 = 9

11
1³ + 5³ + 3³ = 153
1 + 125 + 27 = 153

12
3³ + 7³ + 0³ = 370
27 + 343 + 0 = 370

13
3³ + 7³ + 1³ = 371
27 + 343 + 1 = 371

14
4³ + 0³ + 7³ = 407
64 + 0 + 343 = 407

15
1⁴ + 6⁴ + 3⁴ + 4⁴ = 1634
1 + 1296 + 81 + 256 = 1634

16
8⁴ + 2⁴ + 0⁴ + 8⁴ = 8208
4096 + 16 + 0 + 4096 = 8208

17
9⁴ + 4⁴ + 7⁴ + 4⁴ = 9474
6561 + 256 + 2401 + 256 = 9474

18
5⁵ + 4⁵ + 7⁵ + 4⁵ + 8⁵ = 54748
3125 + 1024 + 16807 + 1024 + 32768 = 54748

19
9⁵ + 2⁵ + 7⁵ + 2⁵ + 7⁵ = 92727
59049 + 32 + 16807 + 32 + 16807 = 92727

20
9⁵ + 3⁵ + 0⁵ + 8⁵ + 4⁵ = 93084
59049 + 243 + 0 + 32768 + 1024 = 93084

21
5⁶ + 4⁶ + 8⁶ + 8⁶ + 3⁶ + 4⁶ = 548834
15625 + 4096 + 262144 + 262144 + 729 + 4096 = 548834

22
1⁷ + 7⁷ + 4⁷ + 1⁷ + 7⁷ + 2⁷ + 5⁷ = 1741725
1 + 823543 + 16384 + 1 + 823543 + 128 + 78125 = 1741725

23
4⁷ + 2⁷ + 1⁷ + 0⁷ + 8⁷ + 1⁷ + 8⁷ = 4210818
16384 + 128 + 1 + 0 + 2097152 + 1 + 2097152 = 4210818

24
9⁷ + 8⁷ + 0⁷ + 0⁷ + 8⁷ + 1⁷ + 7⁷ = 9800817
4782969 + 2097152 + 0 + 0 + 2097152 + 1 + 823543 = 9800817

25
9⁷ + 9⁷ + 2⁷ + 6⁷ + 3⁷ + 1⁷ + 5⁷ = 9926315
4782969 + 4782969 + 128 + 279936 + 2187 + 1 + 78125 = 9926315

26
2⁸ + 4⁸ + 6⁸ + 7⁸ + 8⁸ + 0⁸ + 5⁸ + 0⁸ = 24678050
256 + 65536 + 1679616 + 5764801 + 16777216 + 0 + 390625 + 0 = 24678050

27
2⁸ + 4⁸ + 6⁸ + 7⁸ + 8⁸ + 0⁸ + 5⁸ + 1⁸ = 24678051
256 + 65536 + 1679616 + 5764801 + 16777216 + 0 + 390625 + 1 = 24678051

28
8⁸ + 8⁸ + 5⁸ + 9⁸ + 3⁸ + 4⁸ + 7⁸ + 7⁸ = 88593477
16777216 + 16777216 + 390625 + 43046721 + 6561 + 65536 + 5764801 + 5764801 = 88593477

===

29
1⁹ + 4⁹ + 6⁹ + 5⁹ + 1⁹ + 1⁹ + 2⁹ + 0⁹ + 8⁹ = 146511208
1 + 262144 + 10077696 + 1953125 + 1 + 1 + 512 + 0 + 134217728 = 146511208

30
4⁹ + 7⁹ + 2⁹ + 3⁹ + 3⁹ + 5⁹ + 9⁹ + 7⁹ + 5⁹ = 472335975
262144 + 40353607 + 512 + 19683 + 19683 + 1953125 + 387420489 + 40353607 + 1953125 = 472335975

31
5⁹ + 3⁹ + 4⁹ + 4⁹ + 9⁹ + 4⁹ + 8⁹ + 3⁹ + 6⁹ = 534494836
1953125 + 19683 + 262144 + 262144 + 387420489 + 262144 + 134217728 + 19683 + 10077696 = 534494836

32
9⁹ + 1⁹ + 2⁹ + 9⁹ + 8⁹ + 5⁹ + 1⁹ + 5⁹ + 3⁹ = 912985153
387420489 + 1 + 512 + 387420489 + 134217728 + 1953125 + 1 + 1953125 + 19683 = 912985153

Duration: 3167s


"""

#The example below implements the narcissistic function described in the definition above to search for narcissistic functions #and cycles in Python.
"""
def ppdif(x, b):
    y = x
    digit_count = 0
    while y > 0:
        digit_count = digit_count + 1
        y = y // b
    total = 0
    while x > 0:
        total = total + pow(x % b, digit_count)
        x = x // b
    return total

def ppdif_cycle(x, b):
    seen = []
    while x not in seen:
        seen.append(x)
        x = ppdif(x, b)
    cycle = []
    while x not in cycle:
        cycle.append(x)
        x = ppdif(x, b)
    return cycle

#
#The following Python program determines whether the integer entered is a Narcissistic / Armstrong number or not.
#

def no_of_digits(num):
    i = 0
    while num > 0:
        num //= 10
        i+=1

    return i

def required_sum(num):
    i = no_of_digits(num)
    s = 0
    
    while num > 0:
        digit = num % 10
        num //= 10
        s += pow(digit, i)
        
    return s


num = int(input("Enter number:"))
s = required_sum(num)
     
if s == num:
    print("Armstrong Number")
else:
    print("Not Armstrong Number")
    
"""    
    
    
