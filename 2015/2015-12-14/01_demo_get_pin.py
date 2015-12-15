#!/usr/bin/env python3
#
# Program: demo_get_pin.py
# Objective: Use Rpi.GPIO.gpio_function to get connector pins status.
#
# Written for: Hamilton Python User Group - Presentation 14 December 2015
#              https://github.com/hampug   http://www.meetup.com/nzpug-hamilton/
#               
# Copyright:   This work is licensed under a Creative Commons 
#              Attribution-ShareAlike 4.0 International License.
#              http://creativecommons.org/licenses/by-sa/4.0/
# Author: Ian Stewart
# Date: 2015-12-14

# Imports
import RPi.GPIO as gpio

# Assign variables and constants
pin_function = {0:"OUT", 1:"IN", 40:"SERIAL", 41:"SPI", 42:"I2C", 43:"HARD_PWM"}
gpio.setmode(gpio.BOARD)

print("Obtain the current status of the GPIO pins\n")
max_pin = 0
return_string = input('Does this Raspberry have a 26 pin GPIO connector?[Y/n]:')
if return_string == "":
    max_pin = 26
else:
    if return_string.lower()[0] in ["y", "t", "1"]:
        max_pin = 26
    else:
        max_pin = 40

print("Pin Signal     Value")
for pin in range(1, max_pin + 1):
    try:
        func = gpio.gpio_function(pin)
        print("{:>2}: {:<10} {:>2}".format(pin, pin_function[func], func))
    except:
    	print("{:>2}: VCC or GND".format(pin))

return_string = input('\nType Return to end program...')

'''
pin_function = {0:"OUT", 1:"IN", 40:"SERIAL", 41:"SPI", 42:"I2C", 43:"HARD_PWM"}

	OUT                           : 0
	IN                            : 1
	SERIAL                        : 40
	SPI                           : 41
	I2C                           : 42
	HARD_PWM                      : 43

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

$ python3 demo_get_pin.py
Does this Raspberry have a 26 pin GPIO connector?[Y/n]:y
Pin Signal     Value
 1: VCC or GND
 2: VCC or GND
 3: IN          1
 4: VCC or GND
 5: IN          1
 6: VCC or GND
 7: IN          1
 8: SERIAL     40
 9: VCC or GND
10: SERIAL     40
11: IN          1
12: IN          1
13: IN          1
14: VCC or GND
15: IN          1
16: IN          1
17: VCC or GND
18: IN          1
19: IN          1
20: VCC or GND
21: IN          1
22: IN          1
23: IN          1
24: IN          1
25: VCC or GND
26: IN          1

'''
