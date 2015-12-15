#!/usr/bin/env python3
#
# Program: demo_ttk_pwm_linear.py
#
# Objective: Use a GUI as the loop, and control PWM frequency and duty cycle.
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
frequency = 1  # 1Hz. 
duty_cycle = 50  # percent

PIN_ADDRESSING_METHOD = "BOARD"  # or BCM
SIGNAL = 11  # For BOARD method this is the P1 connector Pin number. 
             # For BCM it is the signal number used by the BCM chip.
             # E.g. BCM signal 17 is the equivalent of BOARD pin 11

TITLE_1 = "Pulse Width Modulation -  Linear Scale"
TITLE_2 = "Pulse Width Modulation GUI application for Raspberry Pi"
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
from subprocess import Popen, PIPE

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

class PWM:
    def __init__(self, master, pwm_channel):
        self.master = master
        master.title(TITLE_1)
        
        # Set font and font size size of all buttons and labels, etc.        
        self.style = ttk.Style()
        # Change a root style to modify all widgets.
        self.style.configure('.', font=('FreeSans', 12))        

        # Widgets for Frequency
        self.label_frequency_1 = ttk.Label(master, text="Frequency")
        self.label_frequency_2 = ttk.Label(master, text="")
        self.scale_frequency = ttk.Scale(master, from_=1, to=100, 
                command=self.scale_frequency_change, orient=HORIZONTAL, 
                length=200, value = frequency * 10)

        # Widgets for Duty Cycle
        self.label_duty_cycle_1 = ttk.Label(master, text="Duty Cycle")
        self.scale_duty_cycle = ttk.Scale(master, from_=0, to=100, 
                command=self.scale_duty_cycle_change, orient=HORIZONTAL, 
                length = 200, value= duty_cycle)
        self.label_duty_cycle_2 = ttk.Label(master, text="")

        # Button to Start
        self.button_start = ttk.Button(master, text="Start", 
                command=self.button_start)
        # Button to Stop
        self.button_stop = ttk.Button(master, text="Stop", 
                command=self.button_stop)
        # Button to close
        self.button_close = ttk.Button(master, text="Close", 
                command=self.button_close)

        # Information labels 
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
        mem_size = "Total Memory:{}".format(get_memory_size())
        py_version = "Python version:{}".format(sys.version.split(" ")[0])
        info_3 = "{}. {}. {}".format(py_version, INFO_3, mem_size)
        self.label_info_3 = ttk.Label(master, text=info_3)

        # Add widgets to grid
        # Slider Frequency
        self.label_frequency_1.grid(row=0, column=0, sticky=W,
                padx=10, pady=10)
        self.label_frequency_2.grid(row=0, column=2, sticky=W,
                padx=10, pady=10)
        self.scale_frequency.grid(row=0, column=1, sticky=W, 
                padx=10, pady=10)
        # Slider Duty Cycle
        self.label_duty_cycle_1.grid(row=1, column=0, sticky=W,
                padx=10, pady=10)
        self.label_duty_cycle_2.grid(row=1, column=2, sticky=W,
                padx=10, pady=10)
        self.scale_duty_cycle.grid(row=1, column=1, sticky=W,
                padx=10, pady=10)
        # Buttons
        self.button_start.grid(row=2,column=0, sticky=W,
                padx=10, pady=10)
        self.button_stop.grid(row=2,column=1,
                padx=10, pady=10)
        self.button_close.grid(row=2,column=2, sticky=E,
                padx=10, pady=10)
        # Info Labels
        self.label_info_1.grid(row=3, column=0, columnspan=3, sticky=W,
                padx=5, pady=5)
        self.label_info_2.grid(row=4, column=0, columnspan=3, sticky=W,
                padx=5, pady=5)
        self.label_info_3.grid(row=5, column=0, columnspan=3, sticky=W,
                padx=5, pady=5)

        #Set initial Frequency and Duty Cycle using the callback
        self.scale_frequency_change(frequency * 10) # 10 = 1Hz
        self.scale_duty_cycle_change(duty_cycle)

    def scale_frequency_change(self, value):
        '''Update display and adjust frequency.'''
        frequency = int(float(value))/10  # 1.2
        period = self.get_period_as_string(frequency)
        self.label_frequency_2.config(text="{:.1f}Hz. {}"
                .format(frequency, period)) 
        # Change the frequency
        # GPIO.PWM(SIGNAL, frequency).ChangeFrequency(frequency)
        pwm_channel.ChangeFrequency(frequency)

    def scale_duty_cycle_change(self, value):
        '''Update display and adjust PWM duty cycle.'''
        duty_cycle = int(float(value))
        # Display the duty cycle
        self.label_duty_cycle_2.config(text="{0:.0f}%".format(duty_cycle))
        # Change the Duty Cycle
        # GPIO.PWM(SIGNAL, frequency).ChangeDutyCycle(duty_cycle)
        pwm_channel.ChangeDutyCycle(duty_cycle)

    def button_start(self):
        '''Start PWM also requires resetting the frequency'''
        # GPIO.PWM(channel, frequency).start(duty_cycle)
        pwm_channel.start(duty_cycle)
        # The start does not maintain the previously assigned frequency. Need 
        # to do a ChangeFrequency to reset to previous frequency. Bug???
        frequency = self.get_frequency() 
        pwm_channel.ChangeFrequency(frequency)

    def button_stop(self):
        '''Stop the PWM'''
        # GPIO.PWM(channel, frequency).stop()
        pwm_channel.stop()

    def button_close(self):
        '''Cleanup PWM and close the GUI'''
        gpio.cleanup()
        root.destroy()
        sys.exit()

    def get_frequency(self):
        '''
        The slide returns a floating point value in the range 1 to 100. Change
        this to an integer and reduce by 1/10th. So range is from 0.1 to 10.
        '''
        #print(self.scale_frequency['value'])
        scale_value = self.scale_frequency['value']
        frequency = int(float(scale_value))/10  # 1.2
        return frequency

    def get_period_as_string(self, frequency):
        '''Given the frequency calculate period and display in Secs or mSecs'''
        period = 1/frequency  # 0.8333333333333334     
        if period >= 1:
            period_string = "Period:{:.2f}Sec".format(period)
        else:
            period = period * 1000
            period_string = "Period:{:.0f}mSec".format(period)
        return period_string

def get_memory_size():
    '''As general information. Get the total memory size'''
    mem = Popen(["cat", "/proc/meminfo"], stdout=PIPE)
    output = mem.communicate()[0]
    for line in output.splitlines():
        if 'MemTotal:' in line.decode('ascii'):
            mem_list = line.decode('ascii').split(" ")
            return "{} {}".format(mem_list[-2],mem_list[-1])

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

    # Setup board pin for the PWM output
    gpio.setup(SIGNAL, gpio.OUT)

    # Instantiate pwm_channel
    pwm_channel = gpio.PWM(SIGNAL,1)  # Initialize at 1Hz

    # Launch tkinter GUI.
    root = Tk()
    #root.geometry('400x80+50+50')
    main_gui = PWM(root, pwm_channel)
    root.mainloop()

'''
Notes:
The frequency slider values are 10 times the frequency. i.e. They range from
1 to 100 to give frequencies of 0.1Hz to 10Hz.

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
