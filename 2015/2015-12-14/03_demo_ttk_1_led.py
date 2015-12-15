#!/usr/bin/env python3
#
# Program: demo_ttk_led_1.py
#
# Objective: Turn on and off a LED
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
#
PIN_ADDRESSING_METHOD = "BOARD"  # or BCM
SIGNAL = 11  # For BOARD method this is the P1 connector Pin number. 
             # For BCM it is the signal number used by the BCM chip.
             # E.g. BCM signal 17 is equivalent of BOARD pin 11

TITLE_1 = "LED On/Off"
TITLE_2 = "LED on/off application for Raspberry Pi"
INFO_1A = ("RPi.GPIO method of pin addressing:{}. Using P1 connector pin:{}"
                .format(PIN_ADDRESSING_METHOD, SIGNAL))
INFO_1B = ("RPi.GPIO method of signal addressing:{}. Using BCM chip signal "
                "number:{}".format(PIN_ADDRESSING_METHOD, SIGNAL))

INFO_2A = ("3.3Volts P1 Connector Pin:1 --> 330ohm resistor --> LED --> P1 "
                "Connector Pin:{}".format(SIGNAL))
INFO_2B = ("3.3Volts P1 Connector Pin:1 --> 330ohm resistor --> LED --> P1 "
                "Connector pin for BCM signal channel:{}".format(SIGNAL))

# Import modules and perform checks
import sys
import os

# Check Python is version 3
if int(sys.version[0]) < 3:
    print("Python Version Error: Run program using python3 to support "
            "tkinter.\nExiting...")
    sys.exit()
    
# RPi.GPIO module
try:
    import RPi.GPIO as gpio
except ImportError as e:  # No module named 'RPi':
    print("Import Error: RPi.GPIO module is not available for importing.\n"
            "This program requires being run on a Raspberry Pi with the "
            "python module RPi.GPIO installed.")
    sys.exit()
    
# Check RPi.GPIO is >= 0.6. 
# From 0.6 onward there is no need for sudo priv in order to run RPi.GPIO
# programs. Prior to version 0.6 programs recieved the message:
# RuntimeError: No access to /dev/mem.  Try running as root!
if float(gpio.VERSION[0:3]) >= 0.6:
    INFO_3 = "Python module RPi.GPIO revision:{}".format(gpio.VERSION)
else:
    print("Error: RPi.GPIO module is at version:{} \n"
            "This program requires version 0.6.0a3 or higher.\n"
            "Raspian from 21 Nov 2015 onward includes a suitable version of RPi.GPIO."
            .format(gpio.VERSION))
    sys.exit()
    
# tkinter and ttk
try:
    from tkinter import *
except ImportError as e:
    print("Import Error: tkinter module for python3 is not available.")
    sys.exit()
try:
    from tkinter import ttk
except ImportError as e:
    print("Import Error: tkinter.ttk module is not available.")    
    sys.exit()

class LED:
    def __init__(self, master):
        self.master = master
        master.title(TITLE_1)
        
        # Set font and font size size of all buttons and labels, etc.        
        self.style = ttk.Style()
        # Change a root style to modify all widgets.
        self.style.configure('.', font=('FreeSans', 12))

	# Create Widgets
        # Button to On
        self.button_on = ttk.Button(master, text="On", 
                command=self.button_on)
        # Button to Off
        self.button_off = ttk.Button(master, text="Off", 
                command=self.button_off)
        # Button to close
        self.button_close = ttk.Button(master, text="Close", 
                command=self.button_close)

        # Information labels 
        #label_info_0 - Mode and signal
        self.label_info_0 = ttk.Label(master, text="Command:")

        #label_info_1 - Mode and signal
        if PIN_ADDRESSING_METHOD == "BOARD": 
            info_1 = INFO_1A
        if PIN_ADDRESSING_METHOD == "BCM": 
            info_1 = INFO_1B
        self.label_info_1 = ttk.Label(master, text=info_1)

        # label_info_2 - Circuit diagram
        if PIN_ADDRESSING_METHOD == "BOARD": 
            info_2 = INFO_2A
        if PIN_ADDRESSING_METHOD == "BCM": 
            info_2 = INFO_2B
        self.label_info_2 = ttk.Label(master, text=info_2)

        # label_info_3 - General Info
        py_version = "Python version:{}".format(sys.version.split(" ")[0])
        info_3 = "{}. {}".format(py_version, INFO_3)
        self.label_info_3 = ttk.Label(master, text=info_3)

        # Add widgets to grid
        # Buttons
        self.button_on.grid(row=2,column=0, sticky=W,
                padx=10, pady=10)
        self.button_off.grid(row=2,column=1,
                padx=10, pady=10)
        self.button_close.grid(row=2,column=2, sticky=E,
                padx=10, pady=10)

        # Info Labels
        self.label_info_0.grid(row=0, column=0, columnspan=3, sticky=W,
                padx=5, pady=5)
        self.label_info_1.grid(row=3, column=0, columnspan=3, sticky=W,
                padx=5, pady=5)
        self.label_info_2.grid(row=4, column=0, columnspan=3, sticky=W,
                padx=5, pady=5)
        self.label_info_3.grid(row=5, column=0, columnspan=3, sticky=W,
                padx=5, pady=5)

    def button_on(self):
        """Turn on LED"""
        gpio.output(SIGNAL, False)
        self.label_info_0.config(text="Command: gpio.output({}, False)"
                .format(SIGNAL))

    def button_off(self):
        """Turn off LED"""
        gpio.output(SIGNAL, True) 
        self.label_info_0.config(text="Command: gpio.output({}, True)"
                .format(SIGNAL))

    def button_close(self):
        """Cleanup PWM and close the GUI"""
        gpio.cleanup()
        root.destroy()
        sys.exit()

if __name__ == "__main__":
    """Setup and instantiate GPIO, then launch tkinter GUI"""
    print(TITLE_2)
    # Turn off warnings...
    # May report "This channel is already in use continuing anyway."
    gpio.setwarnings(False)

    if (not PIN_ADDRESSING_METHOD == "BOARD" and 
        not PIN_ADDRESSING_METHOD == "BCM"):
        print("Invalid Pin addressing method: {}. Use BOARD or BCM."
                 .format(PIN_ADDRESSING_METHOD))
        sys.exit()

    # Set the method python uses of addressing the signals / P1 connector pins.
    mode = "gpio.{}".format(PIN_ADDRESSING_METHOD)
    gpio.setmode(eval(mode))
    if gpio.getmode() == gpio.BOARD:
        print("Pin numbering is set to BOARD")  # 10
    if gpio.getmode() == gpio.BCM:
        print("Signal numbering is set to BCM")  # 11
        sys.exit("Exiting...")

    # Setup board pin for the PWM output
    gpio.setup(SIGNAL, gpio.OUT)

    # Turn off all 4 leds before starting
    led_list = [15, 13, 12, 11]
    gpio.setup(led_list, gpio.OUT)
    gpio.output(led_list, True) 

    # Launch tkinter GUI.
    root = Tk()
    #root.geometry('400x80+50+50')
    main_gui = LED(root)
    root.mainloop()

'''
Notes:

References:
http://sourceforge.net/p/raspberry-gpio-python/wiki/Home/
http://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
http://sourceforge.net/p/raspberry-gpio-python/wiki/Checking%20function%20of%20GPIO%20channels/
https://python-textbok.readthedocs.org/en/1.0/Introduction_to_GUI_Programming.html
http://stackoverflow.com/questions/17125842/python-3-tkinter-change-label-text
http://raspi.tv/2013/how-to-use-soft-pwm-in-rpi-gpio-pt-2-led-dimming-and-motor-speed-control
https://learn.sparkfun.com/tutorials/raspberry-gpio/python-rpigpio-api
https://www.tcl.tk/man/tcl8.5/TkCmd/contents.htm

         1         2         3         4         5         6         7         8
12345678901234567890123456789012345678901234567890123456789012345678901234567890

'''
