#!/usr/bin/env python3
#
# Program Name: circle_4.py, author, date, comments, copyright, etc.
#
# Import modules
from circle_2 import *
from circle_3 import Circle
#print(dir(Circle)) # View functions in the modules Circle class.

# Initialize variables
self = None
# Assigning to constants
TITLE = "Circle Program 4 - Module"

if __name__ == "__main__":
    """Use Circle class to display circumference and area"""
    print(TITLE)
    # perform the calculations from imported circle_2.py module
    r = get_radius()
    print("Using: from circle_2 import *...")
    c,a = calculate_circle(r)
    display_results(r,c,a)

    # perform the calculations from imported circle_3.py module
    print("Using: from circle_3 import Circle...")
    #r = Circle.get_radius()
    c,a = Circle.calculate_circle(self, r)
    Circle.display_results(self, r,c,a)


"""
print(dir(Circle))
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'calculate_circle', 'display_results', 'get_radius']
"""

    

