#!/usr/bin/env python3  # shebang
#
# Program Name: circle_2, author, date, comments, copyright, etc.
#
# Import modules
import math
#
# Initialize variables
radius = 1

# Assigning to constants
TITLE = "Circle Program 2 - Function"

# Program functions
def get_radius():
    """Get the radius"""
    radius = float(input("Enter the radius of the circle:"))
    return radius

def calculate_circle(radius):
    """Perform the circle calculations"""
    circumference = 2 * math.pi * radius
    area = math.pi * radius ** 2
    return circumference, area

def display_results(radius, circumference, area):
    """Display the circles"""
    print("Radius:{}, Circumference:{:.3f}, Area:{:.3f}"
		  .format(radius, circumference, area))

if __name__ == "__main__":
    """Display title, get radius, perform calculations, display result"""
    print(TITLE)
    r = get_radius()
    c,a = calculate_circle(r)
    display_results(r,c,a)

    
