#!/usr/bin/env python3
# Program:  circle3.py
# Author:   Ian Stewart - August 2016
# Copyright: CC0 https://creativecommons.org/publicdomain/zero/1.0/
# Import modules
import math
import sys
# Define constants and variables
DEFAULT_PROMPT = 10
debug = False

def input_radius(prompt):
    """Get User input from the console."""
    radius = input("Enter the radius of the circle [{}]: ".format(prompt))
    if radius == "":
        radius = prompt
    try:
        return float(radius)
    except:
        print("Radius of {} is an invalid value. Exiting...".format(radius))
        sys.exit()

def calculate_circle_area(radius):
    """Supplied with the radius, calculate the area of a circle."""
    area = math.pi * radius ** 2
    if debug:print("Debug Info. Radius: {} Area: {}".format(radius, area))
    return area

def help():
    print("Program to calculate the area of a circle.\n"
          "Supports passing a default radius value from the command line.")
if __name__ == "__main__":
    """Launch circle program."""
    prompt = DEFAULT_PROMPT
    if len(sys.argv) > 1:
        if "-h" in sys.argv[1]:
            help()
            sys.exit()
        if "-d" in sys.argv[1]:
            debug=True
        else:
            prompt = sys.argv[1]
    radius = input_radius(prompt)
    circle_area = calculate_circle_area(radius)
    print("Circle with a radius of {:.2f} has an area of {:.2f}."
          .format(radius, circle_area))
                                                                          

