#!/usr/bin/env python3
#
# kaprekar_constant.py
#
# Constants are 495 for 3 digits and 6174 for 4 digits.
# E.g. 2060 is 6200 - 0026 = 6174
#
# Examples of launching the program...
# $ python kaprekar_constant.py 105
# $ python kaprekar_constant.py 1963
# $ python kaprekar_constant.py
#
# Ian Stewart 2022-10-22
#
import sys
VERBOSE = True
MAX_ITERATIONS = 10

def main(integer_str):
    """
    Recieve integer as string from command line interface
    Call functions to rearrange in descending and ascending orders
    Call function to subtract descending for ascending.
    Loop is not repeating.
    """

    if VERBOSE: print("Initial integer:        {:>8}".format(integer_str))
    
    count = 0
    previous_str = integer_str
    
    while True:
        count += 1
        if VERBOSE: print("\nIteration count:        {:>8}".format(count))

        integer_descend_str = sort_integer_in_descending_order(integer_str)
        if VERBOSE: print("Rearranged decending:   {:>8}".format(integer_descend_str))

        integer_ascend_str = sort_integer_in_asscending_order(integer_descend_str)
        if VERBOSE: print("Rearranged accending:   {:>8}".format(integer_ascend_str))

        integer_str = subtract_descend_from_ascend(integer_descend_str, integer_ascend_str)
        if VERBOSE: print("Sutraction result:      {:>8}".format(integer_str))

        if integer_str == "000" or integer_str == "0000":
            break

        # Exit if repeating sequence s not found by MAX_ITERATIONS.
        if count == MAX_ITERATIONS:
            break

        # If  iteration happens twice in sequence, then exit
        if integer_str == previous_str:   
            if VERBOSE: print("Repeating sequence was reached...")
            break
                                
        else:
            previous_str = integer_str
            continue
            
    return count, integer_str


def sort_integer_in_descending_order(int_str):
    """
    Sort string descending order. E.g. 4557 becomes 7554
    """
    int_descend_str = "".join(sorted(int_str, reverse=True))
    return int_descend_str


def sort_integer_in_asscending_order(int_descend_str):
    """
    Reverse the order of the descending string
    """    
    int_ascend_str = int_descend_str[::-1]
    return int_ascend_str


def subtract_descend_from_ascend(int_descend_str, int_ascend_str):
    """
    Subtract small integer from large integer
    If subtraction result is zero then integer contains the same digits, so exit.
    Else return integer as a zero filled string.
    """
    integer = (int(int_descend_str) - int(int_ascend_str))
    if integer == 0:
        print("Initial integer can not be all the same digit.")
        #sys.exit("Initial integer can not be all the same digit.")
         
    int_str = str(integer)
    length = len(int_descend_str)
    return int_str.zfill(length)


def check_argument(int_str):
    """
    Check if string is a series of digits that make a positive integer.
    """
    try:
        integer = int(int_str)
    except:
        print("Must be an integer")
        sys.exit("Exiting...")

    if integer < 0:
        print("Number must not be negative.")
        sys.exit("Exiting...")

    return int_str


if __name__=="__main__":

    print("\nKaprekar Constant")
    
    # All 3 x digit and 4 x digit analysis
    if len(sys.argv) == 1:
        VERBOSE = False
        for i in range(100, 10000):        
            i_str = str(i)
            int_str = check_argument(i_str)
            #int_str = int_str.zfill(4)
            counter, integer_str = main(int_str)
            print(str(i).zfill(len(i_str)), counter -1, integer_str)        
        
    # Use the sys.argv[1] argument as the data and provide verbose analysis
    if len(sys.argv) >  1:
        int_str = check_argument(sys.argv[1])
        counter, integer_str = main(int_str)
        
        if counter == MAX_ITERATIONS:
            print("After {} iterations there is no repeating sequence"
                    .format(MAX_ITERATIONS))
        
        else:
            print("\n{} took {} iterations to reach a repeating {}"
                    .format(int_str, counter -1, integer_str ))


"""
Reference: 
https://en.wikipedia.org/wiki/Kaprekar%27s_routine

Leading zeroes retained

def digit_count(x, b):
    count = 0
    while x > 0:
        count = count + 1
        x = x // b
    return count
    
def get_digits(x, b, init_k):
    k = digit_count(x, b)
    digits = []
    while x > 0:
        digits.append(x % b)
        x = x // b
    for i in range(k, init_k):
        digits.append(0)
    return digits
    
def form_number(digits, b):
    result = 0
    for i in range(0, len(digits)):
        result = result * b + digits[i]
    return result
    
def kaprekar_map(x, b, init_k):
    descending = form_number(sorted(get_digits(x, b, init_k), reverse=True), b)
    ascending = form_number(sorted(get_digits(x, b, init_k)), b)
    return descending - ascending
    
def kaprekar_cycle(x, b):
    x = int (str(x), b)
    init_k = digit_count(x, b)
    seen = []
    while x not in seen:
        seen.append(x)
        x = kaprekar_map(x, b, init_k)
    cycle = []
    while x not in cycle:
        cycle.append(x)
        x = kaprekar_map(x, b, init_k)
    return cycle


"""
