#/usr/bin/env python3
#
# TODO: Game with going through a maze.
# TODO: Numbers incrementing like a naturla spiral.
#
# narcissistic.py
#
#Python
#
#The example below implements the narcissistic function described in the definition above to search for narcissistic functions #and cycles in Python.
'''
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
"""
for i in range(373):
    if i == ppdif(i,10):
        s = "Narcissistic Number"
    else:
        s = ""
    print(i, ppdif(i, 10), s)
"""

for i in range(373):
    x = ppdif_cycle(i,10)
    print(i, x)

"""
368 755
369 972
370 370
371 371
372 378
"""    
'''
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
 

# Largest. 39 Digits    
# 115,132,219,018,763,992,565,095,597,973,971,522,401
# 115132219018763992565095597973971522401  

# 116000000000000000000000000000000000000  

    
