#!/usr/bin/env python3
#
# Program:      cadence_hampug_demo.py
# Objective:    Demonstrate a function that provides data entry from a terminal.
#               Refer to function "def query()"
#               Uses the gearing on a bike as the example.
# Presention:   Hamilton Python User Group meeting 14 Sep 2015.
#               Used in Accessibility for Visually Impaired presentation. 
#               https://github.com/HamPUG/
# Author:       Ian Stewart
# Date:         2015-09-14
# Portability:  Linux - Tested on Vinux V5.0 beta, based on Ubuntu 14.04.
# Requires:     Python3 - Untested but will probably OK with python v2.7+
# Disk Access:  Creates the text file ~/.local/share/bike/cadence.conf
#               which is used to provide default prompt values for next pass.
# Indentation:  Spaces x 4
#
# Import python modules
import sys
import os
import time
from math import pi

# Exit if python less than version 3.0.0
if sys.hexversion < 0x03000000:
    print('\nPython3 is required. Please restart using Python3.')
    print('Version {0} of python not supported. Exiting...\n'.format(
            sys.version[0:sys.version.find(" ")]))
    sys.exit()

# Initialize Constants and variables
PROGRAM_VERSION = "1.0"
PROGRAM_IDENTIFICATION = "Bike Cadence to Speed calculator"
PROGRAM_SPONSOR = ("""Hamilton Python User Group - https://github.com/HamPUG/
HamPUG is sponsored by Waikato University Department of Computer Science.
Hamilton, New Zealand.""")             
INCH2CM = float(2.54)
CM2INCH = float(1 / 2.54)  # 0.393700787
PAUSE = float(0.5) # Delay after each question for text to speach clarity

# Path and file name to store default values fo use on next pass
hd = os.path.expanduser('~')
data_path = ".local/share/bike/"
data_file = "cadence.conf"

# Ratios of shimano hubs
# https://en.wikipedia.org/wiki/Shimano_Alfine
# http://www.sheldonbrown.com/nexus8.shtml#range
gear_11 = [0.527, 0.681, 0.770, 0.878, 0.995, 1.134, 1.292, 1.462, 1.667, 
            1.888, 2.153]
gear_8 = [0.527, 0.644, 0.748, 0.851, 1.000, 1.223, 1.419, 1.615]
gear_7 = [0.632, 0.741, 0.843, 0.989, 1.145, 1.335, 1.545]

# list of hubs 0 to 2
hub_list = [gear_7, gear_8, gear_11]
hub_name_list = ["7 gear", "8 gear", "11 gear"]

# Define and load with initial data the default values for when a query is posed.
initial_data = []
initial_data.append(PROGRAM_IDENTIFICATION)
initial_data.append(PROGRAM_VERSION)
initial_data.append(True) # Use inches for diameter of wheel
initial_data.append(20)   # 20 inch diameter wheel
initial_data.append(float( 1 / pi * 100)) # 31.83~cm gives circumference of 1m 
initial_data.append(33)   # Chain ring
initial_data.append(18)   # hub input sprocket
initial_data.append(30)   # hub output sprocket
initial_data.append(25)   # axle sprocket
initial_data.append(2)    # Hub Selected
initial_data.append(8)    # Gear selected
initial_data.append(80)   # Cadence

#Constants for pointing into the data list
PROGRAM_ID = 0
VERSION = 1
IS_INCH = 2
DIAMETER_INCH = 3
DIAMETER_CM = 4
COG1 = 5
COG2 = 6
COG3 = 7
COG4 = 8
HUB = 9
GEAR = 10
CADENCE = 11

#===== -h or --help Information =====
PROGRAM_INFO = """
This python script features the function query() that is an enhancement of
the python3 input() function or the python2 raw_input() function.

In posing a query to the console terminal window a query string must be 
supplied and a default return value may be included. The type of data that must
be returned from the keyboard is specified to be either integer, floating 
point, boolean, or the default of a string. Failure to enter from the keyboard
the correct data type will result in the returned data being rejected and the 
query posed again. Wrong data type entries may occur until the retry limit is
reached. The default number of retries is 3. 

Upon exceeding the retry limit a return value will be supplied. In the case
of a boolean data type then False is returned. In the case of integer and
floating point data types the value of 1 is returned. No check is performed to
determine if a value of 1 is outside of the minimum and maximum limits if 
they have been specified.

For integer and floating point data types it is optional to specify the minimum
or maximum limits of the input returned from the keyboard. If the keyboard 
input is a value outside the minimum or maximum values, then the user is
informed of this error, and the query is supplied again.

When a string data type is specified, then anything returned from the keyboard
is accepted.

The default return value is normally shown in square brakets at the end of the 
query line. This can be changed to be at the front of the query line by setting
the 'order' argument to false. 

If a text-to-speech screen reader is being used clarity of what is being 
spoken can be lost as one query is immediately followed by another query. To
overcome this a slight delay is injected prior to the keyboard entry response 
is returned. The pause is set to 0.5 of a second.
  
The following is an example of a function that sets up the arguments and then
makes the call to the query function:

def get_teeth_on_sprocket():
    '''Retrieve the number of teeth on the chain ring sprocket.'''
    prompt_ = 'teeth on chain ring sprocket. Or select new value'
    def_ = "30"
    type_ = "integer"
    min_ = 20
    max_ = 100
    is_norm_ = False
    attempts_ = 5  
    return query(prompt_, def_, type_, min_, max_, is_norm_, attempts_)

The above will display:
[30] teeth on chain ring sprocket. Or select new value:

This program was written to aid in the design of a human powered vehicle. It 
provides for modelling the pedalling cadence and gear ratios to determine the
speed. The program was used by a designer who is blind and uses the program 
with a text-to-speech screen reader.
"""

#===== Function to query user =====
def query(prompt, default_response = "", data_type = "string", 
            minimum = None, maximum = None, order=True, retry = 3):
    """
    Pose a query on the gui terminal window and ensure data returned from the 
    keyboard is suitable. Returned data can be either: string, float, integer, 
    or boolean. The default data type is a string.
    For Float and Integer queries, minimum and maximum values may be specified.
    The order on the line of the prompt and the default value may be switched.
    Allows a limited number of retries to correctly enter the type of data.
    PAUSE = 0.5 # Allow a delay after each question for text to speech clarity.
    Ref: https://docs.python.org/3/library/stdtypes.html#typesnumeric
    """
    PAUSE = 0.5
    # Place square brackets around the default value
    if default_response != "":
        if order:
            default = (" [{0}]".format(default_response))
        else:
            default = ("[{0}] ".format(default_response))        
    
    # Get input from keyboard allowing retries if input data is invalid.     
    while retry != 0:
        # Query order can be Prompt and Default (normal) or Default and Prompt.
        if order:
            # Provide for python2 using "raw_input", which is python3 "input".       
            if int(sys.version[0]) < 3:
                return_string = raw_input("\n{0}{1}: ".format(prompt, default))      
            else:        
                return_string = input("\n{0}{1}: ".format(prompt, default))
        else:
            # Provide for python2 using raw_input, which is python3 input
            if int(sys.version[0]) < 3:
                return_string = raw_input("\n{0}{1}: ".format(default, prompt))      
            else:        
                return_string = input("\n{0}{1}: ".format(default, prompt))
        
        # Strip the newline character and any leading or trailing white space    
        return_string = return_string.strip() #rstrip('\n') #strip only newline

        # Check returned string from the keyboard is valid data
        # Returns: string, floating, integer, boolean
        if data_type == "string":
            # Accept any data. If response is none return the default_response. 
            if default_response == "":
                time.sleep(PAUSE)
                return default_response
                break                
            else:
                time.sleep(PAUSE)
                return return_string
                break

        if data_type == "boolean":
            # Define, in lower case, the True and False lists 
            bool_true = ["y", "t", "1"]
            bool_false = ["n", "f", "0"]

            # On an empty return allow default. Use first letter of default
            if return_string == "":
                bool_string = default_response.lower()[:1]
            else:
                # Extract the first letter in lower case
                bool_string = return_string.lower()[:1]
            
            # Assign a return of True or False, or repeat the query.
            if bool_string in bool_true:     
                time.sleep(PAUSE)
                return True
                break            
            elif bool_string in bool_false:     
                time.sleep(PAUSE)
                return False
                break 
            else:
                print("{} is not valid boolean response.".format(return_string))
                retry -=  1
                if retry == 0:
                    print("Exhausted retries. Returning boolean of False")
                    time.sleep(PAUSE)
                    return False
                    break
                else:
                    continue

        if data_type == "integer":
            if return_string == "":
                return_string = default_response
            try:
                int(return_string)
                return_integer = int(return_string)
            except ValueError:
                print("{} is not an integer.".format(return_string))
                retry -=  1
                if retry == 0:
                    print("Exhausted retries. Returning number of 1")
                    time.sleep(PAUSE)
                    return 1
                    break
                else:
                    continue
            if minimum != None:
                if return_integer < minimum:
                    print("{0} is less than the minimum of {1}."
                            .format(return_integer, minimum))
                    retry -=  1
                    if retry == 0:
                        print("Exhausted retries. Returning number of 1")
                        time.sleep(PAUSE)
                        return 1
                        break
                    else:
                        continue
            if maximum != None:               
                if return_integer > maximum:
                    print("{0} is greater than the maximum of {1}."
                            .format(return_integer, maximum))
                    retry -=  1
                    if retry == 0:
                        print("Exhausted retries. Returning number of 1")
                        time.sleep(PAUSE)
                        return 1
                        break
                    else:
                        continue  
            # Within the minimum and maximum bounds, if used, so return integer
            time.sleep(PAUSE)
            return return_integer

        if data_type == "floating":
            if return_string == "":
                return_string = default_response            
            # Test if return string is a floating point number.
            try:
                float(return_string)
                return_float = float(return_string)
            except ValueError:
                print("{} is not a floating point number.".format(return_string))
                retry -=  1
                if retry == 0:
                    print("Exhausted retries. Returning number of 1")
                    time.sleep(PAUSE)
                    return 1.0
                    break
                else:
                    continue
            if minimum != None:
                if return_float < minimum:
                    print("{0} is less than the minimum of {1}."
                            .format(return_float, minimum))
                    retry -=  1
                    if retry == 0:
                        print("Exhausted retries. Returning number of 1")
                        time.sleep(PAUSE)
                        return 1.0
                        break
                    else:
                        continue
            if maximum != None:                
                if return_float > maximum:
                    print("{0} is greater than the maximum of {1}."
                            .format(return_float, maximum))
                    retry -=  1
                    if retry == 0:
                        print("Exhausted retries. Returning number of 1")
                        time.sleep(PAUSE)
                        return 1.0
                        break
                    else:
                        continue
            # Within the minimum and maximum bounds, if used, so return float 
            time.sleep(PAUSE)
            return return_float

        # Date Type is not: string, boolean, integer or floating. 
        # i.e. Typo in date_type argument?
        time.sleep(PAUSE)
        return return_string

#===== Functions to set up each call to the main query function =====
def get_measurement_units(data):     
    """Query if input of wheel diameter is to be in inches. Return T/F."""
    prompt_ = "Do you want to use inches for the wheel diameter?"
    if data[IS_INCH]:
        def_ = "Yes"
    else:
        def_ = "No" 
    type_ = "boolean"
    min_ = None
    max_ = None
    is_norm_ = True
    retry_ = 3
    data[IS_INCH] = query(prompt_, def_, type_, min_, max_, is_norm_, retry_)    
    return data

def get_wheel_diameter(data):
    """Retrieve the wheel diameter in eith inches or centimeters."""
    if data[IS_INCH]:
        prompt_ = "inch diameter wheel. Or enter the new value"
        def_ = data[DIAMETER_INCH] #"20"
        type_ = "floating"
        min_ = 1
        max_ = None  
        is_norm_ = False
        data[DIAMETER_INCH] = query(prompt_, def_, type_, min_, max_, is_norm_)
        data[DIAMETER_CM] = data[DIAMETER_INCH] * INCH2CM    

    else:
        prompt_ = "centimeter diameter wheel. Or enter the new value"
        def_ = data[DIAMETER_CM] #"31.83098861837907"  
        type_ = "floating"
        min_ = 1
        max_ = None
        is_norm_ = False
        data[DIAMETER_CM] = query(prompt_, def_, type_, min_, max_, is_norm_)
        data[DIAMETER_INCH] = data[DIAMETER_CM] * CM2INCH
    return data

def get_cog1(data):
    """Retrieve the number of teeth on the chain ring sprocket."""
    prompt_ = "teeth on chain ring sprocket. Or select new value"
    def_ = data[COG1] #"30"
    type_ = "integer"
    min_ = 1
    max_ = None
    is_norm_ = False  
    data[COG1] = query(prompt_, def_, type_, min_, max_, is_norm_)
    return data
    #print(data[COG1])

def get_cog2(data):
    """Retrieve the number of teeth on the input to the gear hub."""
    prompt_ = "teeth on the hub input sprocket. Or select new value"
    def_ = data[COG2] #"18"
    type_ = "integer"
    min_ = 1
    max_ = None
    is_norm_ = False  
    data[COG2] = query(prompt_, def_, type_, min_, max_, is_norm_)
    return data
    #print(data[COG2])

def get_cog3(data):
    """Retrieve the number of teeth on the gear hub output sprocket."""
    prompt_ = "teeth on the hub output sprocket. Or select new value"
    def_ = data[COG3] #"30"
    type_ = "integer"
    min_ = 1
    max_ = None
    is_norm_ = False  
    data[COG3] = query(prompt_, def_, type_, min_, max_, is_norm_)
    return data
    #print(data[COG3])

def get_cog4(data):
    """Retrieve the number of teeth on the rear axle."""
    prompt_ = "teeth on the rear axle sprocket. Or select new value"
    def_ = data[COG4] #"25"
    type_ = "integer"
    min_ = 1
    max_ = None
    is_norm_ = False  
    data[COG4] = query(prompt_, def_, type_, min_, max_, is_norm_)
    return data
    #print(data[COG4])

def get_hub_type(data):
    """Pick type of Shimano hub to be use based on th given number."""
    prompt_ = "selected. 1 = 7 gear hub, 2 = 8 gear hub, 3 = 11 gear hub"
    def_ = data[HUB] #2
    type_ = "integer"
    min_ = 1
    max_ = 3
    is_norm_ = False  
    data[HUB] =  query(prompt_, def_, type_, min_, max_, is_norm_)
    return data
    #print(data[HUB])

def get_gear(data, hub_selected_list):
    """Select the gear to be used"""
    prompt_ = ("gear is selected. Or select new gear in range 1 to {}"
                .format(len(hub_selected_list)))
    def_ = data[GEAR] # 8. 1 to 7, 7 or 11. 7_gear, 8_gear,  11_gear
    type_ = "integer"
    min_ = 1
    max_ = len(hub_selected_list)
    is_norm_ = False  
    data[GEAR] = query(prompt_, def_, type_, min_, max_, is_norm_)
    return data
    #print(data[GEAR])

def get_cadence(data):
    """Get the pedalling cadence. Pedalling revolutions per minute"""
    prompt_ = "cadence. Or select new value"
    def_ = data[CADENCE] #"80"
    type_ = "integer"
    min_ = 1
    max_ = None
    is_norm_ = False  
    data[CADENCE] = query(prompt_, def_, type_, min_, max_, is_norm_)
    return data
    #print(data[CADENCE])

# ===== Start of storage of default data functions =====
def create_default_data_file(init_data):
    """
    If a file containing the default values for queries does not exist then
    create one and fill with the initial data.
    """
    #hd = os.path.expanduser('~')
    # If file does not exist create path then add file with data
    if not os.path.isfile(os.path.join(hd, data_path, data_file)):
        print("Default data file doesn't exit, creating one.")
        try:
            os.makedirs(os.path.join(hd, data_path), exist_ok=True)        
        except:
            print("Unable to create path {}{}" .format(hd,datapath)) 

        with open(os.path.join(hd, data_path, data_file), 'w') as f: 
            for item in init_data:            
                f.write("{}{}".format(item, "\n"))
                f.closed

    else:
        # Data file exists, check it matches the version of this program.
        with open(os.path.join(hd, data_path, data_file), 'r') as f:
            line1 = f.readline()[:-1] # should be PROGRAM_IDENTIFICATION
            line2 = f.readline()[:-1] # should be PROGRAM_VERSION as string.
            f.closed

        #print('Line2:{}, Program Version:{}'.format(line2, PROGRAM_VERSION))
        if line2 != PROGRAM_VERSION:
            # delete the data file and exit
            os.remove(os.path.join(hd, data_path, data_file))
            sys.exit("Error: Wrong data file for this version. Please restart")

        #print("File existed")
        #print(init_data)  

def load_data_from_file():
    if os.path.isfile(os.path.join(hd, data_path, data_file)):
        #print("opening file")
        with open(os.path.join(hd, data_path, data_file), 'r') as f:
            data = []
            #print(data) # []
            #print(len(f))
            for line in f:
                line = line.rstrip()
                data.append(line)
                #print(line)
            f.closed
    else:
        print("Unable to open cadence.conf data file")

    #Convert the string data to float or integer, as required.
    #print(data)
    data[DIAMETER_INCH] = float(data[DIAMETER_INCH])
    data[DIAMETER_CM] = float(data[DIAMETER_CM])
    for i in range(COG1, len(data)):
        data[i] = int(data[i])
    #print(data)
    return data

def store_default_data(data):
    data[DIAMETER_CM] = float(1/pi * 100) # Force a circumference of 1 meter
    #print(data)
    with open(os.path.join(hd, data_path, data_file), 'w') as f: 
        for item in data:            
            f.write("{}{}".format(item, "\n"))
            f.closed

# ===== Main Program flow ====
def main():
    """
    Main program flow.
    All calculations in this function are metric."""
    
    #home = os.path.expanduser("~")
    #data_path = ".local/share/bike/"
    #data_file = "cadence.conf"
    #Location of default data: ~/.local/share/bike/cadence.conf

    # ===== Start of default data file section =====
    create_default_data_file(initial_data)
  
    # The file exists and is either the initial data or previous pass data. 
    data = load_data_from_file()
    # ===== End of Default data file section =====

    # ===== Start of User entry section =====
    data = get_measurement_units(data)
    

    # Return the wheel diameter in meters
    data = get_wheel_diameter(data)
    # Convert diameter into meters
    diameter = data[DIAMETER_CM] / 100

    # Get the number of teeth on the 4 sprockets
    data = get_cog1(data)
    
    data = get_cog2(data)
    
    data = get_cog3(data)
    
    data = get_cog4(data)
    
    # Select the type of hub and which gear of the selected hub
    data = get_hub_type(data)
    
    #hub_list = [gear_7, gear_8, gear_11]
    hub_selected_list = hub_list[data[HUB] - 1]
    #hub_name_list = ["7 gear", "8 gear", "11 gear"]
    hub_name = hub_name_list[data[HUB] - 1]

    # Prevent having a default value that exceeds the gears on the hub
    if data[GEAR] > len(hub_selected_list):
        data[GEAR] = len(hub_selected_list)

    data = get_gear(data, hub_selected_list)
    
    gear_ratio = hub_selected_list[data[GEAR] -1]

    # Get the cadence - Peddling speed per minute
    data = get_cadence(data)
    
    #===== End of User Data Entry =====
 
    #===== Start of Calculations and Output =====
    # Note: float() added below so python2 wont default to integer division.
    print("")

    print("{} tooth chain ring sprocket to {} tooth hub input sprocket is "
            "one to {:.3f}."
            .format(data[COG1], data[COG2], data[COG1]/float(data[COG2])))

    print("{} tooth hub output sprocket to the {} tooth axle sprocket is one "
            "to {:.3f}."
            .format(data[COG3], data[COG4], data[COG3]/float(data[COG4])))

    print("With the {} hub in gear number {} the ratio is one to {}."
            .format(hub_name, data[GEAR], gear_ratio))

    # Calculate the overall combined ratio of the sprockets and gears.
    #oa_ratio = (cog1/float(cog2)) * (cog3/float(cog4)) * gear_ratio

    oa_ratio = ((data[COG1]/float(data[COG2])) * (data[COG3]/float(data[COG4]))
                 * gear_ratio)

    # Calculate the rpm of the rear axle
    rear_axle_rpm = data[CADENCE] * oa_ratio
    # Calculate the circumference of the rear wheel in meters.
    circumference = diameter * pi
    # Calculate the speed of the rear wheel in kilo-meters per hour
    speed = (circumference * rear_axle_rpm * 60) / 1000

    print("")
    if data[IS_INCH]:
        wheel = ("{} inch".format(data[DIAMETER_INCH]))
    else:
        wheel = ("{} centimeter".format(data[DIAMETER_CM]))

    print("With a cadence of {} and an overall ratio of {:.3f}\n"
            "the speed of the {} wheel is:\n"
            "{:.3f} kilometers per hour.\n"
            .format(data[CADENCE], oa_ratio, wheel, speed))

    #===== End of Calculations and Output =====
    
    #===== Store the data so it is the default on the next pass ====
    store_default_data(data)
  
    print("\nFinished.")
    sys.exit()

if __name__ == "__main__":
    """Launch main program or provide the help information"""
    print("\n{}. Version {}".format(PROGRAM_IDENTIFICATION, PROGRAM_VERSION))
    
    if len(sys.argv) == 2:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("\n{}".format(PROGRAM_INFO))
            sys.exit()

    print("{}".format(PROGRAM_SPONSOR))
    print("Restart with --help argument for information about this program.")
    main()

 
"""
Notes:

Wheel diameter in centimeters: 31.83098861837907 = 1 meter circumference
Use this diameter to verify the mathematics.

# Examples of using the query function
# Arguments: (prompt, default = "", data_type = "string", , 
#       minimum = None, maximum = None, order="normal" retry = 3)
#returned = query("Enter your name", "", "string")
#returned = query("Do you want anything?", "Yes/No", "boolean")
#returned = query("Do you want anything?", "Yes/No", "boolean")
#returned = query("Pick a number", 15, "integer-typo")
#returned = query("Pick a floating number", 15.2, "floating", 1.5, 2.1)
#returned = query("Is the number?", 5, "integer", 0 , 10, False, 5)
#print(returned)  

Example:

$ python3 cadence_hampug_demo.py

Bike Cadence to Speed calculator. Version 1.0
Hamilton Python User Group - https://github.com/HamPUG/
HamPUG is sponsored by Waikato University Department of Computer Science.
Hamilton, New Zealand.
Restart with --help argument for information about this program.

Do you want to use inches for the wheel diameter? [Yes]: 

[20.0] inch diameter wheel. Or enter the new value: 

[33] teeth on chain ring sprocket. Or select new value: 

[18] teeth on the hub input sprocket. Or select new value: 

[30] teeth on the hub output sprocket. Or select new value: 

[25] teeth on the rear axle sprocket. Or select new value: 

[2] selected. 1 = 7 gear hub, 2 = 8 gear hub, 3 = 11 gear hub: 

[8] gear is selected. Or select new gear in range 1 to 8: 

[80] cadence. Or select new value: 

33 tooth chain ring sprocket to 18 tooth hub input sprocket is one to 1.833.
30 tooth hub output sprocket to the 25 tooth axle sprocket is one to 1.200.
With the 8 gear hub in gear number 8 the ratio is one to 1.615.

With a cadence of 80 and an overall ratio of 3.553
the speed of the 20.0 inch wheel is:
27.218 kilometers per hour.


Finished.
$ 
"""
