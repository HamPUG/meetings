#!/usr/bin/python3
#
# Program: demo_rpi_package.py
#
# Objective: Introduce the RPi.GPIO module
#
# Written for: Hamilton Python User Group - Presentation 14 December 2015
#              https://github.com/hampug   http://www.meetup.com/nzpug-hamilton/
#               
# Copyright:   This work is licensed under a Creative Commons 
#              Attribution-ShareAlike 4.0 International License.
#              http://creativecommons.org/licenses/by-sa/4.0/
# Author: Ian Stewart
# Date: 2015-12-14
#
#        1         2         3         4         5         6         7         8
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
#
# Use constants for the introductory text.
INFO_1 = '''
demo_rpi_package.py
This program introduces the python package (RPi) for the General Purpose Input 
and Output (GPIO) of the Raspberry Pi. On a Raspberry Pi the P1 connector is 
comprised of either 26 pins in two rows for the original models A and B, or 
40 pins in two rows for the newer models.
'''

INFO_2 = '''
To view all the attributes of the GPIO module:
$ python3
Python 3.2.3 (default, Mar  1 2013, 11:53:50) 
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import RPi.GPIO
>>> dir(RPi.GPIO)
['BCM', 'BOARD', 'BOTH', 'FALLING', 'HARD_PWM', 'HIGH', 'I2C', 'IN', ...etc. 
'''

INFO_3 = '''
To obtain help on a specific attribute. 
An example of retrieving the help information on the PWM attribute:
>>> import RPi.GPIO
>>> help()
help> RPi.GPIO.PWM
Help on class PWM in RPi.GPIO:

RPi.GPIO.PWM = class PWM(builtins.object)
 |  Pulse Width Modulation class
... etc. (Note: Type q to quit the help)
'''

INFO_4 = '''
In using python or python3 GPIO module it is recommended that it be imported as:
import RPi.GPIO as gpio
'''

INFO_5 = '''
The release of RPi.GPIO revision 0.6.0a3 removed the need to run programs with
sudo priv. Raspian images from 21 November 2015 included RPi.GPIO 0.6 or higher.
If running RPi.GPIO below revision 0.6 upgrading is recommended. To check the
revision of RPi.GPIO.
$ python3
Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
[GCC 4.9.1] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from RPi.GPIO import gpio
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: cannot import name 'gpio'
>>> import RPi.GPIO as gpio
>>> gpio.VERSION
'0.6.0a3'
'''

INFO_6 = '''
Please scroll back and review the information this program produced and use it 
as a reference when running the other demonstration programs.

'''
# Import modules
try:
    import RPi.GPIO as gpio
except:
    print("Package: RPi, module: GPIO, not available to be imported.")
    sys.exit("Exiting")

import sys
print('RPi.GPIO package information.')
s = input('\nPaused to allow you to adjust window width to 132 columns.\n'
          'Press Return key to continue...')

# Obtain from a Package a specific modules attributes
# Define the package and module
attribute_list = dir(gpio)
# Make a backup copy of the attributes for tracking purposes
attribute_list_copy  = dir(gpio)
PACKAGE = "RPi"
MODULE = "GPIO"
ALIAS = "gpio"
# Print the introductory information
print(INFO_1)
print(INFO_2)
print(INFO_3)
print(INFO_4)
print(INFO_5)
print("The following is a dynamically generated breakdown of the RPi.GPIO "
      "attributes:")

# Turn off warning message that occurs when gpio.cleanup() performed.
gpio.setwarnings(False)

print("\n{} package".format(PACKAGE))
print("{}.{} total attributes = {}".format(PACKAGE, MODULE, len(attribute_list)))

# <class 'int'>
counter = 0
for index, attribute in enumerate(attribute_list):
    module_attribute = "{}.{}".format(ALIAS, attribute)
    attribute_type = "type({})".format(module_attribute)
    if str(eval(attribute_type)) == "<class 'int'>":
        counter +=1
        #Print the Heading
        if counter == 1:
            print("\n{} class int".format(MODULE))
        # Print the integer class attribute and its value
        print("\t{0:<30}: {1:}"
                .format(attribute_list[index], eval(module_attribute)))
	# Track the listing of attributes, remove the item from the backup copy
        attribute_list_copy.remove(attribute)
# Print the total in thie class
string = "Total <class int>"
print("\t{0:<30}= {1:}".format(string, counter))

# <class 'str'>
counter = 0
for index, attribute in enumerate(attribute_list):
    module_attribute = "{}.{}".format(ALIAS, attribute)
    attribute_type = "type({})".format(module_attribute)
    if str(eval(attribute_type)) == "<class 'str'>":
        counter +=1
        if counter == 1:
            print("\n{} class str".format(MODULE))
        print("\t{0:<30}: {1:}"
                .format(attribute_list[index], eval(module_attribute)))
        attribute_list_copy.remove(attribute)
string = "Total <class str>"
print("\t{0:<30}= {1:}".format(string, counter))

# <class 'dict'>
counter = 0
for index, attribute in enumerate(attribute_list):
    module_attribute = "{}.{}".format(ALIAS, attribute)
    attribute_type = "type({})".format(module_attribute)
    if str(eval(attribute_type)) == "<class 'dict'>":
        counter +=1
        if counter == 1:
            print("\n{} class dict".format(MODULE))
        print("\t{}:".format(attribute_list[index]))
        for key, value in eval(module_attribute).items():
            print("\t\t{0:<30}: {1:}".format(key, value))
        attribute_list_copy.remove(attribute)
string = "Total <class dict>"
print("\t{0:<30}= {1:}".format(string, counter))

# <class 'builtin_function_or_method'>
counter = 0          
for index, attribute in enumerate(attribute_list):
    module_attribute = "{}.{}".format(ALIAS, attribute)
    attribute_type = "type({})".format(module_attribute)
    if str(eval(attribute_type)) == "<class 'builtin_function_or_method'>":
        counter +=1
        if counter == 1:
            print("\n{} class builtin_function_or_method".format(MODULE))

	# Determine min number of arguments the function supports or requires
        error_string = ""
        try:
            # Enter invalid argument to force failure
            eval("{}.{}()".format(ALIAS, attribute))
            error_string = "0 arguments"
        except TypeError as error:
            #print(error)
            # Strip any "(0 given)" and "not found" from the error message)
            error_string = str(error)
            error_string = error_string.replace(" (0 given)", "", 1)
            error_string = error_string.replace(" not found", "", 1)
        argument_min = error_string
	# Determine max number of arguments the function supports or requires
        try:
            # Enter invalid argument to force failure
            eval("{}.{}(9,9,9,9,9,9,9,9,9,9)".format(ALIAS, attribute))
            error_string = "0 arguments"
        except TypeError as error:
            #print(error)
            # Strip the (10 given from the error message)
            error_string = str(error)
            error_string = error_string.replace(" (10 given)", "", 1)
        argument_max = error_string
        # Avoid repetative data
        if argument_min == argument_max:
            argument_max = ""
        else: 
            argument_max = " / " + argument_max 
        print("\t{0:<30}: {1:}{2:}"
                .format(attribute_list[index], argument_min, argument_max))
        attribute_list_copy.remove(attribute)
string = "Total <class type>"
print("\t{0:<30}= {1:}".format(string, counter))

# <class 'type'>
counter = 0
for index, attribute in enumerate(attribute_list):
    module_attribute = "{}.{}".format(ALIAS, attribute)
    attribute_type = "type({})".format(module_attribute)
    if str(eval(attribute_type)) == "<class 'type'>":
        counter +=1
        if counter == 1:
            print("\n{} class type".format(MODULE))
        print("\t{}".format(attribute_list[index]))
        attribute_list_copy.remove(attribute)
string = "Total <class type>"
print("\t{0:<30}= {1:}".format(string, counter))

#<class 'NoneType'>
counter = 0
for index, attribute in enumerate(attribute_list):
    module_attribute = "{}.{}".format(ALIAS, attribute)
    attribute_type = "type({})".format(module_attribute)
    #print(str(eval(attribute_type)))
    if str(eval(attribute_type)) == "<class 'NoneType'>":
        counter +=1
        if counter == 1:
            print("\n{} class NoneType".format(MODULE))
        print("\t{}".format(attribute_list[index]))
        attribute_list_copy.remove(attribute)
string = "Total <class NoneType>"
if counter != 0:
    print("\t{0:<30}= {1:}".format(string, counter))

counter = 0
if len(attribute_list_copy) != 0:
    print("\nRemaining classes = {}".format(len(attribute_list_copy)))
    #for item in attribute_list_copy:
        #print(item)
    for index, attribute in enumerate(attribute_list_copy):    
        module_attribute = "{}.{}".format(ALIAS, attribute)
        attribute_type = "type({})".format(module_attribute)
        print("\t{0:<30}: {1:}".format(attribute, str(eval(attribute_type))))        
    
print(INFO_6)

return_string = input('\nType return to end program...')
sys.exit()

'''

Sample program output to the console:

pi@raspberrypi:~ $ python3 demo_rpi_package.py
demo_rpi_package.py
This program introduces the python package (RPi) for the General Purpose Input 
and Output (GPIO) of the Raspberry Pi. On a Raspberry Pi the P1 connector is 
comprised of either 26 pins in two rows for the original models A and B, or 
40 pins in two rows for the newer models.


To view all the attributes of the GPIO module:
$ python3
Python 3.2.3 (default, Mar  1 2013, 11:53:50) 
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import RPi.GPIO
>>> dir(RPi.GPIO)
['BCM', 'BOARD', 'BOTH', 'FALLING', 'HARD_PWM', 'HIGH', 'I2C', 'IN', ...etc. 


To obtain help on a specific attribute. 
An example of retrieving the help information on the PWM attribute:
>>> import RPi.GPIO
>>> help()
help> RPi.GPIO.PWM
Help on class PWM in RPi.GPIO:

RPi.GPIO.PWM = class PWM(builtins.object)
 |  Pulse Width Modulation class
... etc. (Note: Type q to quit the help)


In using python or python3 GPIO module it is recommended that it be imported as:
import RPi.GPIO as gpio


The release of RPi.GPIO revision 0.6.0a3 removed the need to run programs with
sudo priv. Raspian images from 21 November 2015 included RPi.GPIO 0.6 or higher.
If running RPi.GPIO below revision 0.6 upgrading is recommended. To check the
revision of RPi.GPIO.
$ python3
Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
[GCC 4.9.1] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from RPi.GPIO import gpio
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: cannot import name 'gpio'
>>> import RPi.GPIO as gpio
>>> gpio.VERSION
'0.6.0a3'

The following is a dynamically generated breakdown of the RPi.GPIO attributes:

RPi package
RPi.GPIO total attributes = 40

GPIO class int
	BCM                           : 11
	BOARD                         : 10
	BOTH                          : 33
	FALLING                       : 32
	HARD_PWM                      : 43
	HIGH                          : 1
	I2C                           : 42
	IN                            : 1
	LOW                           : 0
	OUT                           : 0
	PUD_DOWN                      : 21
	PUD_OFF                       : 20
	PUD_UP                        : 22
	RISING                        : 31
	RPI_REVISION                  : 2
	SERIAL                        : 40
	SPI                           : 41
	UNKNOWN                       : -1
	Total <class int>             = 18

GPIO class str
	VERSION                       : 0.6.0a3
	__doc__                       : GPIO functionality of a Raspberry Pi using Python
	__file__                      : /usr/lib/python3/dist-packages/RPi/GPIO.cpython-34m-arm-linux-gnueabihf.so
	__name__                      : RPi.GPIO
	__package__                   : RPi
	Total <class str>             = 5

GPIO class dict
	RPI_INFO:
		REVISION                      : 000f
		RAM                           : Unknown
		PROCESSOR                     : Unknown
		TYPE                          : Unknown
		MANUFACTURER                  : Unknown
		P1_REVISION                   : 2
	Total <class dict>            = 1

GPIO class builtin_function_or_method
	add_event_callback            : Required argument 'gpio' (pos 1) / function takes at most 2 arguments
	add_event_detect              : Required argument 'gpio' (pos 1) / function takes at most 4 arguments
	cleanup                       : 0 arguments / function takes at most 1 argument
	event_detected                : function takes exactly 1 argument
	getmode                       : 0 arguments
	gpio_function                 : function takes exactly 1 argument
	input                         : function takes exactly 1 argument
	output                        : function takes exactly 2 arguments
	remove_event_detect           : function takes exactly 1 argument
	setmode                       : function takes exactly 1 argument
	setup                         : Required argument 'channel' (pos 1) / function takes at most 4 arguments
	setwarnings                   : function takes exactly 1 argument
	wait_for_edge                 : Required argument 'channel' (pos 1) / function takes at most 4 arguments
	Total <class type>            = 13

GPIO class type
	PWM
	Total <class type>            = 1

Remaining classes = 2
	__loader__                    : <class '_frozen_importlib.ExtensionFileLoader'>
	__spec__                      : <class '_frozen_importlib.ModuleSpec'>

Please scroll back and review the information this program produced and use it 
as a reference when running the other demonstration programs.


pi@raspberrypi:~ $ 


'''
