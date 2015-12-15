#!/usr/bin/env python3
#
# Program: demo_ttk_2_switches.py
# Objective: Use switches to change GPIO input signals. Turn on and off a LED
#
# Written for: Hamilton Python User Group - Presentation  14 December 2015
#              http://www.hampug.org.nz   http://www.meetup.com/nzpug-hamilton/
#               
# Copyright:   This work is licensed under a Creative Commons 
#              Attribution-ShareAlike 4.0 International License.
#              http://creativecommons.org/licenses/by-sa/4.0/
# Author: Ian Stewart
# Date: 2015-12-14
#
PIN_ADDRESSING_METHOD = "BOARD"  # or BCM
LED_SIGNAL = 11  # For BOARD method this is the P1 connector Pin number. 
             # For BCM it is the signal number used by the BCM chip.
             # E.g. BCM signal 17 is equivalent of BOARD pin 11
SWITCH_1_SIGNAL = 22
SWITCH_2_SIGNAL = 18

TITLE_1 = "GPIO input controlled by 2 x Switches"
TITLE_2 = "Switches turning on/off a LED application for Raspberry Pi"
INFO_1A = ("RPi.GPIO method of pin addressing:{}. Using P1 connector pins:"
           "{}, {}, {}".format(PIN_ADDRESSING_METHOD, LED_SIGNAL,
                               SWITCH_1_SIGNAL, SWITCH_2_SIGNAL))
INFO_1B = ("RPi.GPIO method of signal addressing:{}. Using BCM chip signal "
           "numbers:{}, {}, {}".format(PIN_ADDRESSING_METHOD, LED_SIGNAL,
                                       SWITCH_1_SIGNAL, SWITCH_2_SIGNAL))

INFO_2A = ("3.3Volts P1 Connector Pin:1 --> 330ohm resistor --> LED --> P1 "
                "Connector Pin:{}".format(LED_SIGNAL))
INFO_2B = ("3.3Volts P1 Connector Pin:1 --> 330ohm resistor --> LED --> P1 "
                "Connector pin for BCM signal channel:{}".format(LED_SIGNAL))

INFO_3A = ("3.3Volts P1 Connector Pin:1 --> Switch1 --> P1 "
           "Connector Pin:{} pulled Low"
           .format(SWITCH_1_SIGNAL))
INFO_3B = ("3.3Volts P1 Connector Pin:1 --> Switch1 --> P1 "
           "Connector pin for BCM signal channel:{} pulled Low"
           .format(SWITCH_1_SIGNAL))

INFO_4A = ("A Ground Pin on P1 Connector --> Switch2 --> P1 "
           "Connector Pin:{} pulled High".format(SWITCH_2_SIGNAL))
INFO_4B = ("A Ground Pin on P1 Connector --> Switch2 --> P1 "
           "Connector pin for BCM signal channel:{} pulled High"
           .format(SWITCH_2_SIGNAL))

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
    INFO_5 = "Python module RPi.GPIO revision:{}".format(gpio.VERSION)
else:
    print("Error: RPi.GPIO module is at version:{} \n"
            "This program requires version 0.6.0a3 or higher.\nRaspian "
            "from 21 Nov 2015 onward includes a suitable version of RPi.GPIO."
            .format(gpio.VERSION))
    sys.exit()

# Check that program is run with root priv. Otherwise...
# RuntimeError: No access to /dev/mem.  Try running as root!
# crw-r----T 1 root kmem 1, 1 Jan  1  1970 /dev/mem
if os.geteuid() != 0:
    print("Root priviledge is required for RPi.GPIO using revision 0.6.0a3.\n"
          "Restart the program and prefix the command with 'sudo'.\n"
          "This is to avoid a problem with add_event_detect which may report\n"
          "RuntimeError: Failed to add edge detection.\n"
          "Later revisions of RPi.GPIO may have corrected this problem." )
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
    
class Switch:
    def __init__(self, master):
        self.master = master
        master.title(TITLE_1)

        # Setup Switch 1. Turning on switch connects signal to +3.3V
        gpio.setup(SWITCH_1_SIGNAL,
                   gpio.IN,
                   pull_up_down=gpio.PUD_DOWN)

        # With RPi.GPIO revision 0.6.0a3 the add_event_detect may produce
        # RuntimeError: Failed to add edge detection. Run the program using
        # sudo to avoid this error.
        # Edge detection can be RISING, FALLING or BOTH
        gpio.add_event_detect(SWITCH_1_SIGNAL,
                              gpio.FALLING,
                              bouncetime=300)   
        gpio.add_event_callback(SWITCH_1_SIGNAL,
                                self.switch_1_callback)
        
        # Setup switch 2. Turning on switch connects signal to Ground.
        gpio.setmode(gpio.BOARD)
        gpio.setup(SWITCH_2_SIGNAL,gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(SWITCH_2_SIGNAL,
                              gpio.RISING,
                              callback=self.switch_2_callback,
                              bouncetime=300)
        
        # Set font and font size size of all buttons and labels, etc.        
        self.style = ttk.Style()
        # Change a root style to modify all widgets.
        self.style.configure('.', font=('FreeSans', 12))

	# Create Widgets
        # Button to display switches status
        self.button_on = ttk.Button(master, text="Switches Status", 
                command=self.button_switches_status)
        # Button to dosiplay LED status 
        self.button_off = ttk.Button(master, text="LED status", 
                command=self.button_led_status)

        # Button to close
        self.button_close = ttk.Button(master, text="Close", 
                command=self.button_close)

        # Information labels 
        #label_info_0 - Mode and signal
        self.label_info_0 = ttk.Label(master, text="")

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

        # label_info_3 - Switch1 Info
        if PIN_ADDRESSING_METHOD == "BOARD": 
            info_3 = INFO_3A
        if PIN_ADDRESSING_METHOD == "BCM": 
            info_3 = INFO_3B
        self.label_info_3 = ttk.Label(master, text=info_3)

        # label_info_4 - Switch2 Info
        if PIN_ADDRESSING_METHOD == "BOARD": 
            info_4 = INFO_4A
        if PIN_ADDRESSING_METHOD == "BCM": 
            info_4 = INFO_4B
        self.label_info_4 = ttk.Label(master, text=info_4)

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
        self.label_info_4.grid(row=6, column=0, columnspan=3, sticky=W,
                padx=5, pady=5)

    def switch_1_callback(self, channel):
        '''Switch 1 Tied to VCC. High turn on LED'''
        print("Switch1: Edge Event on channel:{}".format(channel))
        if gpio.input(channel):
            print("Switch1: Input high")
            self.label_info_0.config(text="Switch 1 signal High")
            gpio.output(LED_SIGNAL, False)            
        else:
            print("Switch1: Input low")
            self.label_info_0.config(text="Switch 1 signal Low")
            gpio.output(LED_SIGNAL, True)

    def switch_2_callback(self, channel):
        '''Switch 2 Tied to Ground. Low turn off LED'''
        print("Switch2: Edge Event on channel:{}".format(channel))
        if gpio.input(channel):
            print("Switch2: Input high")
            self.label_info_0.config(text="Switch 2 signal High")
            gpio.output(LED_SIGNAL, False)
        else:
            print("Switch2: Input low")
            self.label_info_0.config(text="Switch 2 signal Low")
            gpio.output(LED_SIGNAL, True)

    def button_switches_status(self):
        """Display the switches status"""
        self.label_info_0.config(text="Switches Signal Status (0=Low 1=High) - "
                                 "Switch 1 (Pin{}): {} - "
                                 "Switch 2 (Pin{}): {}"
                                 .format(SWITCH_1_SIGNAL,
                                         gpio.input(SWITCH_1_SIGNAL),
                                         SWITCH_2_SIGNAL,
                                         gpio.input(SWITCH_2_SIGNAL)))

    def button_led_status(self):
        """Display the LED status""" 
        self.label_info_0.config(text="LED Status (0=Low=On 1=High=Off) - "
                                 "LED Pin{}: {}"
                                 .format(LED_SIGNAL, gpio.input(LED_SIGNAL)))

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
    gpio.setwarnings(True)
    
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


    # Turn off all 4 leds before starting.
    if PIN_ADDRESSING_METHOD == "BOARD":
        led_list = [15, 13, 12, 11]
    else:
        led_list = [22, 27, 18, 17]
    gpio.setup(led_list, gpio.OUT)
    gpio.output(led_list, True) 

    # Setup board pin for a LED to be switched
    gpio.setup(LED_SIGNAL, gpio.OUT)
    
    # Launch tkinter GUI.
    root = Tk()
    #root.geometry('400x80+50+50')
    main_gui = Switch(root)
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
