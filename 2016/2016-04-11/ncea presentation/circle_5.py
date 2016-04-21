#!/usr/bin/env python3
#
# Program Name: circle_5.py, author, date, comments, copyright, etc.
#
# Import modules
from circle_3a import Circle
#print(dir(Circle)) # View functions in the modules Circle class.

# Assigning to constants
TITLE = "Circle Program 5 - Module with @classmethod decorators"

if __name__ == "__main__":
    """Use Circle class to display circumference and area"""
    print(TITLE)
    # perform the calculations from imported circle_3a.py module
    print("Using: from circle_3a import Circle...")
    r = Circle.get_radius()
    c,a = Circle.calculate_circle(r)
    Circle.display_results(r,c,a)


"""
print(dir(Circle))
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'calculate_circle', 'display_results', 'get_radius']
"""

    

