#!/usr/bin/env python3
#
# main_program.py
#
# Calls the file constant.conf, a mock config file for setting User parameters.
# The assumption is the User has legitimate privileges to access and edit the 
# constant.conf file, but does not have priv to access the main_program.py
# file.
# 
# A User could attempt to enter code into the config file which may have a
# malicious impact on the execution of the main program. 
#
# The main_program.py program should contain enough filtering that any 
# malicious code in the constant.conf will not get executed. 
# 
# The config file must only pass and execute constants of the supported types.
#
# A User modifiable constant is all upper case and words may be joined with _
#
# A system constant should not be able to be manipulated by a User from the 
# config file. These constants start with an underscore.
#
# User modifiable constants. Initial default values:
FONT_COLOUR = "red"
MAX_VALUE_INT = 10
MAX_VALUE_FLOAT = 9.9

print("Original value: FONT_COLOUR = ", FONT_COLOUR)
print("Original value: MAX_VALUE_INT = ", MAX_VALUE_INT)
print("original value: MAX_VALUE_FLOAT = ", MAX_VALUE_FLOAT)

# Embedded system constants. User can not modify via config file.
_MIN_VERSION = 3
_MAX_CONSTANT_COUNT = 10
_SUPPORTED_TYPE_LIST = [int, str, float, ]
_SPACES_IN_STRING = False


import sys

class Main():
    def __init__(self):
        """
        User parameters may have been changed by the constant.conf file.
        """
        print("From Main(): FONT_COLOUR = ", FONT_COLOUR)
        print("From Main(): MAX_VALUE_INT = ", MAX_VALUE_INT)
        print("From Main(): MAX_VALUE_FLOAT = ", MAX_VALUE_FLOAT)

        print("The code that continues would now implement these constants.")


def config_file_filtering(line):
    """
    Check each line of the config file. 
    Reject if not a valid constant. 
    Two system constants control type of constants and is strings have spaces:
    _SUPPORTED_TYPE_LIST = [int, str, float, ]
    _SPACES_IN_STRING = True
    """
    #print(line)
    # Get rid of start/end whitespace
    line = line.strip()
    # Ignore lines starting with a comment
    if line.startswith("#"):
        return

    # Split on the assignment of the constant
    line_list = line.split(" = ")

    # There must be two items in the list.
    if len(line_list) != 2:
        return

    # Get the Constant identifier and strip it
    line_0 = line_list[0].strip()
    #print(type(line_0))
    #print(line_0)

    # Reject if its possibly a system constant starting with underscore
    if line_0.startswith("_"):
        return

    # Reject if spaces are in the constant
    if " " in line_0:
        return

    # Reject if the constant identifier is not all uppercase. Allows _
    if not line_0.isupper():
        return
      
    # Get the literal and strip it.
    line_1 = line_list[1].strip()
    #print(type(line_1))
    #print(line_1)

    # What type of constants are acceptable. String, Integer, Float.
    # If line from conf file is of one of the supported data types then proceed.
    for index, data_type in enumerate(_SUPPORTED_TYPE_LIST):
        try:
            if type(eval(line_1)) is data_type:
                break
            else:
                #print(index)
                if index == len(_SUPPORTED_TYPE_LIST) - 1:
                    return
                continue
        except:
            # Eg. NameError: name 'qwerty' is not defined
            return

    # Check literal string is allowed to contain spaces?
    if type(eval(line_1)) is str:
        if not _SPACES_IN_STRING:
            if " " in line_1:
                return

    # Appear to have a valid constant so return it to be executed.
    return line


if __name__ == "__main__":
    # Read the configuration file and implement valid changes to constants.
    # Uses _MAX_CONSTANT_COUNT to avoid case of massive number of constants
    # being fed to this main_program.
    try:
        with open("constant.conf", "r") as fin:
            configuration_list = fin.readlines()
    except:
        configuration_list = []

    count = 0
    for line in configuration_list:
        # Call function to check config file. Only allow constants
        line = config_file_filtering(line)
        if not line:
            continue

        # Confident its assigning a valid constant so Execute
        try:
            exec(line)
        except:
            continue

        # print("Modified constant:", line)
        count += 1
        if count > _MAX_CONSTANT_COUNT:
            print("Error: {} constants. Not accepting any more."
                    .format(_MAX_CONSTANT_COUNT))
            break

    # Check that a system constant executes and has not been changed by conf.
    if sys.version_info.major < _MIN_VERSION:
        sys.exit("Error: Please run python version {} or higher.".
                  format(sys.version_info.major)) 

    # Call main call
    Main()

"""
Summary of checks performed on each line from constant.conf:

constant.conf exists, if not ignore that its not avaialble.
Strip line of whitespace at start and end
Ignore the line if it starts with a comment, i.e. #
Split the line based on " = " being the only valid assigning for a constant.
Ignore the line if split did not return a list of two items.
Preform checks on the namespace of the constant:
    Strip any whitespace
    Ignore the line if it starts with an underscore. i.e. System constant.     
    Ignore the line is there are spaces in the name
    Ignore the line if constant identifier is not all uppercase, but allow _

Perform checks on the literal assigned to the constant:
    Strip literal of any whitespace.
    Check if literal is of a supported data type in _SUPPORTED_TYPE_LIST
    If literal is a string then check _SPACES_IN_STRING bool is applicable.

If the line has made it through the above checks then execute the code and
modify a constant that the main section of code will make use of.

Keep a count of each constant that is modified. Apply the limit on how many
constants may be modified.
"""
