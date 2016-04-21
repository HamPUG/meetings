#!/usr/bin/env python3  # shebang
#
# Program Name: circle_1.py, author, date, comments, copyright, etc.
#
# Import modules
import math
#
# Initialize variables
radius = 1

# Assigning to constants
TITLE = "Circle Program 1 - Simple"

# Program code
print(TITLE)

# Calculate circumference and area
radius = float(input("Enter the radius of the circle:"))
circumference = 2 * math.pi * radius
area = math.pi * radius ** 2

# Display the calculations
print("Radius:{}, Circumference:{:.3f}, Area:{:.3f}"
		.format(radius, circumference, area))

