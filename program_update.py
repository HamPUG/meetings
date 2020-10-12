#!/usr/bin/env python3
#
# program_update.py
#
# Embedded on the last line is the count of times the program has been run.
# Each time the program is run, update the count.
#
# Could almost be called "self-modifying code".
#
# Ian Stewart - 2020-10-09

import sys

PROGRAM_NAME = sys.argv[0]
#
def main():
    "Main program goes here"
    print("The main part of the program is run...")


def program_run_count():
    """
    Keep track of how many times the program is run.
    Last line of program is a comment and an integer. E.g. # 10
    Read the last line and increment the integer.
    """
    with open(PROGRAM_NAME, "r") as fin:
        lines = fin.readlines()

    # Get count from the last line
    line = lines[-1][1:]
    line = line.strip()
    #print(line)
    try:
        value = int(line)    
    except:
        print("Number of times program has been run is not an integer.")
        sys.exit("Exiting...")

    value += 1
    #print(value)
    print("{} has been run {} times".format(PROGRAM_NAME, value))

    # Update number of times program has been run.
    lines[-1] = "# " + str(value) + "\n"

    # Re-write the program with updated count
    with open(PROGRAM_NAME, "w") as fout:
        for line in lines:
            fout.write(line)  


if __name__ == "__main__":
    program_run_count()
    main() 
    print("End of program") 
          
# Number of times the program has been run:
# 0
