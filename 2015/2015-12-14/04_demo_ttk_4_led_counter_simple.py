#!/usr/bin/env python3
#
# Program: demo_ttk_4_led_counter_simple.py
#
# Objective: Use a GUI as the loop. Count 0 to 15 in the leds.
# Uses a led_list to demonstrate multiple signals contorlled in one command.
# E.g. GPIO.output(led_list, True)  # All LEDs off to start.
# The list is constructed as MSB to LSB for simple iteration through the list.
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
# Setup variables and constants.
PIN_ADDRESSING_METHOD = "BOARD"  # or BCM
led_list = [15, 13, 12, 11] # Broadcom BCM GPIO signals. MSB --> LSB
#PIN_ADDRESSING_METHOD = "BCM"  # or BOARD
#led_list = [22, 27, 18, 17] # Broadcom BCM GPIO signals. MSB --> LSB

# Create a string that is a list of the pins / signals for information labels
SIGNAL = ", ".join(map(str,led_list))
                  
TITLE_1 = "LED Counter - Simple: MSB to LSB"
TITLE_2 = "LED Counter GUI application for Raspberry Pi - Simple"
INFO_0 = "Number:"
INFO_1A = ("RPi.GPIO method of pin addressing:{}. Using P1 connector pins:{}"
                .format(PIN_ADDRESSING_METHOD, SIGNAL))
INFO_1B = ("RPi.GPIO method of signal addressing:{}. Using BCM chip signal "
                "numbers:{}".format(PIN_ADDRESSING_METHOD, SIGNAL))

INFO_2A = ("3.3Volts P1 Connector Pin:1 --> 330ohm resistors --> LED's --> P1 "
                "Connector Pins:{}".format(SIGNAL))
INFO_2B = ("3.3Volts P1 Connector Pin:1 --> 330ohm resistors --> LED's --> P1 "
                "Connector based on BCM signal channels:{}".format(SIGNAL))

# Import modules and perform checks
import sys
import os
from time import sleep

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

class LED_Counter:
    def __init__(self, master):
        self.master = master
        master.title(TITLE_1)

        # Set font size and colour of all buttons and labels        
        self.style = ttk.Style()
        self.style.theme_use('default') #'clam', 'alt', 'default', 'classic'
        self.style.configure('TButton',
                             foreground='blue',
                             font=('FreeSans', 16))
        self.style.configure('TLabel',
                             foreground='black',
                             font=('FreeSans', 14))
        # Create a style for the number label
        self.style.configure('number.TLabel',
                             foreground='green',
                             font=('FreeSans', 18))
        
        # Alturnatively, comment out the above styles and just use the following        
        # Change a root style to modify all widgets that have not been modified.
        self.style.configure('.', font=('FreeSans', 12))
        

        # Button to count 0 to 15
        self.button_increment = ttk.Button(master,
                                           text="Count 0 to 15",
                                           command=self.button_count_0_to_15)
        # Button to count 15 to 0
        self.button_decrement = ttk.Button(master,
                                           text="Count 15 to 0",
                                           command=self.button_count_15_to_0)
        # Button to close
        self.button_close = ttk.Button(master,
                                       text="Close",
                                       command=self.button_close)

        # Information labels
        # label info_0
        self.label_info_0 = ttk.Label(master,
                                      text=INFO_0,
                                      style='number.TLabel')        
        
        # label info_1 - Mode and signal
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
        info_3 = "{}. {}.".format(py_version, INFO_3)
        self.label_info_3 = ttk.Label(master, text=info_3)

        # Add widgets to grid
        # Buttons
        self.button_increment.grid(row=2, column=0, sticky=W, padx=10, pady=10)
        self.button_decrement.grid(row=2, column=1, padx=10, pady=10)
        self.button_close.grid(row=2, column=2, sticky=E, padx=10, pady=10)
        
        # Info Labels
        self.label_info_0.grid(row=0, column=1, padx=5, pady=5)        
        self.label_info_1.grid(row=3, column=0, columnspan=3, sticky=W, padx=5,
                               pady=5)
        self.label_info_2.grid(row=4, column=0, columnspan=3, sticky=W, padx=5,
                               pady=5)
        self.label_info_3.grid(row=5, column=0, columnspan=3, sticky=W, padx=5,
                               pady=5)

    def button_count_0_to_15(self):
        '''Start counting up in binary using led_list'''
        counter = 0
        while counter < 16:
            self.label_info_0['text'] = "Number:{}".format(counter)            
            root.update_idletasks()  #Refresh GUI is required. or root.update()
            # Convert counter to 4 character binary. 0000 0001 0010 0011, etc.
            bin_string = "{0:0{1}b}".format(counter, 4)
            #print(bin_string)
            for i in range(len(led_list)):
                gpio.output(led_list[i], not int(bin_string[i])) 
            sleep(1)
            counter +=1

    def button_count_15_to_0(self):
        '''Start counting down in binary using led_list'''
        counter = 16
        while counter:
            counter -=1
            self.label_info_0['text'] = "Number:{}".format(counter)            
            root.update_idletasks()  #Refresh of GUI #root.update()
            # Convert counter to 4 character binary. 1111 1110 1101 1100, etc.
            bin_string = "{0:0{1}b}".format(counter, 4)
            #print(bin_string)
            for i in range(len(led_list)):
                gpio.output(led_list[i], not int(bin_string[i])) 
            sleep(1)

    def button_close(self):
        '''Cleanup GPIO signals and close the GUI'''
        gpio.cleanup()
        root.destroy()
        sys.exit()


if __name__ == "__main__":
    '''Setup and instantiate GPIO, then launch tkinter GUI'''
    print(TITLE_2)
    # Turn off warnings...
    # May report "This channel is already in use continuing anyway."
    gpio.setwarnings(False)

    if (not PIN_ADDRESSING_METHOD == "BOARD" and 
        not PIN_ADDRESSING_METHOD == "BCM"):
        print("Invalid Pin addressing method: {}"
                 .format(PIN_ADDRESSING_METHOD))
        sys.exit()
        
    # Set the method python uses of addressing the signals / P1 connector pins.
    mode = "gpio.{}".format(PIN_ADDRESSING_METHOD)
    gpio.setmode(eval(mode))
    if gpio.getmode() == gpio.BOARD:
        print("Pin numbering is set to BOARD")  # 10
    if gpio.getmode() == gpio.BCM:
        print("Signal numbering is set to BCM")  # 11

    # Setup board pins for the output to the counter LEDS
    gpio.setup(led_list, gpio.OUT)
    
    # All LEDs off to start
    gpio.output(led_list, True)

    # Launch tkinter GUI.
    root = Tk()
    #root.geometry('400x80+50+50')
    main_gui = LED_Counter(root)
    root.mainloop()

'''
Notes:
Pins on P1
     Pin BCM
GEN00 11 17
GEN01 12 18
GEN02 13 27
GEN03 15 22
GEN04 16 23
GEN05 18 24
GEN06 22 25

Pins on P5 Model A and B where P1 is a total of 26 pins.
GEN07 03 28
GEN08 04 29
GEN09 05 30
GEN10 06 31

References:
http://sourceforge.net/p/raspberry-gpio-python/wiki/Home/
http://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
http://sourceforge.net/p/raspberry-gpio-python/wiki/Checking%20function%20of%20GPIO%20channels/
https://python-textbok.readthedocs.org/en/1.0/Introduction_to_GUI_Programming.html
http://stackoverflow.com/questions/17125842/python-3-tkinter-change-label-text
http://raspi.tv/2013/how-to-use-soft-pwm-in-rpi-gpio-pt-2-led-dimming-and-motor-speed-control
https://learn.sparkfun.com/tutorials/raspberry-gpio/python-rpigpio-api
https://www.tcl.tk/man/tcl8.5/TkCmd/contents.htm
'''
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
