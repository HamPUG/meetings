#!/usr/bin/env python3  # shebang
#
# Program Name: circle_3, author, date, comments, copyright, etc.
#
# Import modules
import math
#
# Initialize variables
radius = 1

# Assigning to constants
TITLE = "Circle Program 3 - Class"

class Circle():
    def __init__(self):
        """Control the circle program"""
        r = self.get_radius()
        c,a = self.calculate_circle(r)
        self.display_results(r,c,a)

    @classmethod
    def get_radius(self):
        """Get the radius"""
        radius = float(input("Enter the radius of the circle:"))
        return radius

    def calculate_circle(self, radius):
        """Perform the circle calculations"""
        circumference = 2 * math.pi * radius
        area = math.pi * radius ** 2
        return circumference, area

    def display_results(self, radius, circumference, area):
        """Display the circles"""
        print("Radius:{}, Circumference:{:.3f}, Area:{:.3f}"
		      .format(radius, circumference, area))

if __name__ == "__main__":
    """Use Circle class to display circumference and area"""
    print(TITLE)
    Circle()

    
