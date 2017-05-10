#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# server.py
# Objective:
# Provide a R-Pi server to count input pulses recieved from a rotating wheel.
# Also provide the ability to simlate the pulses if not using a R-Pi computer.
# A repeating timer processes the number of pulses counted in a time period.
# Using the timer period and realtime clock. Calculate distances, speeds, etc.
# Use pydbus so that on command from a client a message list of data is passed.
# Based on examples from: https://github.com/LEW21/pydbus
#
# Ian Stewart
# 2019-05-06
# 
# Importing...
import sys
if int(sys.version[0]) < 3:
    print("Please use python 3.")
    sys.exit("Exiting...")

try:
    from pydbus import SessionBus
except ImportError as e:
    print("Import Error: {}".format(e))
    print("Please install pydbus from PyPI: $ sudo pip3 install pydbus")
    print("Installated into: ~/.local/lib/python3.x/site-packages/pydbus")
    sys.exit("Exiting...")

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib

import threading
import time
import random
import math
import numpy

# If not using a R-Pi then let the server run with simulated pulse data.
simulated_pulse = False
channel = 2
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print("Imported RPi.GPIO module")
except ImportError as e:
    print("Import Error: {}".format(e))
    print("Invoking simulation of GPIO input pulses.")
    simulated_pulse = True

# Variables / Constants / Instantiation
#simulated_pulse = True  # Debug: Overide import RPi.GPIO code above.
loop = GLib.MainLoop()
BUS = "org.freedesktop.velocity.server5"
# Timer to trigger ever n seconds.
period = 1 # seconds between events to analyze data and build latest message.
counter = 0
start_time = 0
event_count = 0 # Total of timer_event callback called. Not currently used
# Running average buffer length
distance_list_length = 4
distance_list = [0] * distance_list_length

pulse_count = 0
message_list = []

# 26 inch bicycle wheel sizes - circumference in meters.
# 26 × 2.10	    2.068
# 26 × 2.125	2.070
# 26 × 2.35	    2.083
# 26 × 3.00	    2.170

# Choose between starting with radius or circumference value.
#wheel_radius = 0.15915494309 # <-- meter radius gives 1 meter circumference.
#wheel_circumference = 2 * math.pi * wheel_radius
wheel_circumference = 1
#wheel_circumference = 2.125 # 26 inch × 2.125
wheel_radius = wheel_circumference / (2 * math.pi)

# Starting...
# Display Version information.
print("Python:{}, GLib:{}.{}.{}, pydbus:0.6.0"
    .format(
    sys.version.split(" ")[0],
    GLib.MAJOR_VERSION, GLib.MINOR_VERSION, GLib.MICRO_VERSION,)
    )
print("server starting...")

def supply_data():
    """
    Supply the list of data to feed to the client
    """
    return ["Hello", "there", "how's", "things?"]

class DBusService(object):
    """ 
    <!-- This doc-string passes the XML. -->
    <node>
        <interface name='org.freedesktop.velocity.server'>
            <!-- Signature of 'ai' for list of signed int 32 bit  integers-->
            <method name='get_integer_data'>
                <arg type='ai' name='response' direction='out'/>
            </method>

            <!-- get_status passes list of strings. Use "as" signature.
                 Passes: ["x", "y"] or message = ["x","y"] -->
            <method name='get_status'>
                <arg type='as' name='response' direction='out'/>
            </method>

            <!-- get_multiple lists passes list of string and int. 
                 Use "(asai) signature.
                 Pass tuple of string and int list (["a","b"],[1, 2]) -->
            <method name='get_multiple_lists'>
                <arg type='(asai)' name='response' direction='out'/>
            </method>

            <!-- get_multiple_lists passes list of string and int. 
                 Use "(asai) signature.
                 Pass tuple calling lists (string(), integer()) -->
            <method name='get_multiple_lists_2'>
                <arg type='(asai)' name='response' direction='out'/>
            </method>

            <method name='echo_string'>
                <arg type='s' name='a' direction='in'/>
                <arg type='s' name='response' direction='out'/>
            </method>
            <method name='info'/>
            <method name='refresh'/>
            <method name='quit'/>
        </interface>
    </node>
    """
    def get_status(self):
        """Return the status of the server as a string list"""
        return message_list #supply_data()

    def get_integer_data(self):
        """
        Return a list of integer data'
        Signature of ai has a range of -2147483648 to 2147483647
        """
        return [-2147483648, 0, 2, 3, 4, 2147483647]

    def get_multiple_lists(self):
        """
        Return a string list and an integer list    
        """
        return (["a", "b", "c"], [1, 2, 3])

    def get_multiple_lists_2(self):
        """
        Perform calls to return a string list and an integer list
        One call is outside the class, the other is inside requiring self.    
        """
        return (supply_data(), self.get_integer_data())

    def echo_string(self, s):
        """
        returns whatever is passed to it
        """
        return s

    def info(self):
        tod_time = time.strftime("%a, %d %b %Y %H:%M:%S", 
                                 time.localtime(start_time))
        message_string = ("Wheel circumference: {} meters\n"
                          "Start time: {}\n"
                          "GPIO Channel Number: {}"
                          .format(wheel_circumference, tod_time, channel))

        bus_1 = SessionBus()
        notifications = bus_1.get('.Notifications')
        notifications.Notify('test', 0, 
                             'dialog-information', 
                             "Pydbus Server Information", 
                             message_string, 
                             [], {}, 5000)

    def refresh(self):
        """
        Set the global counter to 0 to refresh the client GUI
        """
        global counter
        counter = 0
        #print("refresh")

    def quit(self):
        """
        Removes this object from the DBUS connection and exits
        """
        rt.stop()
        loop.quit()
        sys.exit("Server is exiting....")

def pulse_callback(channel):
    """
    Receive pulses on GPIO pin. Count until timer_event resets pulse_count
    """
    global pulse_count
    pulse_count += 1


def timer_event():
    """
    Called at the period set for the RepeatingTimer()
    counter is number of times the timer event has been entered.
    message_string is to be passed to client. on a get_status request.
    """
    global pulse_count
    global message_list    
    global counter # Running total of pulses
    global start_time
    global simulated_pulse
    global event_count # Total of timer_event callback called. Not used.
    event_count += 1

    if counter == 0:
        # Trip has just begun in the last period.
        #print('starting timer')
        start_time = time.time()

    # Replace this with GPIO pulsed data.    
    # Simulate wheel rotation. Generate random integers in a range.
    if simulated_pulse:
        counter_inc_value = random.randint(2, 10)
        counter = counter + counter_inc_value
        # For testing:
        #counter_inc_value = 8
        #counter = counter + counter_inc_value        
    else:
        counter_inc_value = pulse_count
        pulse_count = 0
        counter = counter + counter_inc_value
 
    # Buffer for running average. Shuffle from right to left in the list
    distance_list.append(counter_inc_value * wheel_circumference)
    distance_list.pop(0) 
    #print()
    #print(distance_list)
    # Alternative - shuffling left to right in the list
    #distance_list.insert(0, counter_inc_value)    
    #distance_list.pop()

    # Perform calculations
    # Use counter, time_start, wheel_radius
    # Distance
    #distance = 2 * wheel_radius * math.pi * counter_inc_value
    #total_distance = 2 * wheel_radius * math.pi * counter

    distance = wheel_circumference * counter_inc_value
    total_distance =  wheel_circumference * counter

    #average_distance = numpy.mean(distance_list)
    average_distance = sum(distance_list)/len(distance_list)
   

    # Duration: Requires subtract of period from start time.
    duration = time.time() - (start_time - period) 

    # Average Speed in meter per second.
    speed = distance / period
    total_average_speed = total_distance / duration

    average_speed = average_distance / period

    # Conversion
    # Distance: m. Convert m to km divide by 1000
    # Speed: m/s. Convert m/s to km/h multiply by 3.6
    # Time: s.x Convert seconds.xxx to day, hh:mm:ss
    # int(duration) // 86400 <-- number of days.
    # time.strftime("%H:%M:%S", time.gmtime(666777)) <-- hh:mm:ss
    duration_dhms = ("{}days-{}"
                     .format(int(duration) // 86400,
                     time.strftime("%H:%M:%S", time.gmtime(duration))))

    # message list build. String value counter_inc and elapsed time in seconds
    message_list = []
    message_list.append("{}".format(counter_inc_value))  # 0 Wheel rotations.
    message_list.append("{}".format(period))  # 1

    # Append the message list of string data to go to client.
    # append: distance, speed, speed in kms, 
    message_list.append("{:.1f}".format(distance))  # 2
    message_list.append("{:.1f}".format(speed))  # 3
    message_list.append("{:.1f}".format(speed*3.6))  #4

    # Append: duration s, duration h:m:s:, total_distance, total dist kms, 
    # total_average_speed, total_average_speed kms
    message_list.append("{}".format(int(duration))) # 5
    message_list.append(duration_dhms)  # 6
    message_list.append("{:.1f}".format(total_distance))  # 7
    message_list.append("{:.1f}".format(total_distance/1000))  # 8
    message_list.append("{:.1f}".format(total_average_speed))  # 9 
    message_list.append("{:.1f}".format(total_average_speed * 3.6))  # 10

    # Append: Running averages: distance, speed(m/s) speed km/h, samples
    message_list.append("{:.2f}".format(average_distance))  # 11
    message_list.append("{:.1f}".format(average_speed))  # 12
    message_list.append("{:.1f}".format(average_speed * 3.6))  # 13
    message_list.append("{}".format(len(distance_list)))  # 14
    #print(message_list)    
    # message received on the client after issuing
    # reply = self.server_1_object.get_status() 
    # ['10', '1', '8.0', '8.0', '28.8', '10', '0days-00:00:10', '60.0', '0.1',
    # '5.5', '19.6', '6.50', '6.5', '23.4', '4']


class RepeatedTimer(object):
    """
    Repeating timer. Attempts to prevent drift by using time.time() 
    If there was a delay, it should fire at next correct point in real-time.
    TODO: Compare with GLib.timeout_add( interval, function, parameters)
    """
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
          self.next_call += self.interval
          self._timer = threading.Timer(self.next_call - time.time(), self._run)
          self._timer.start()
          self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

if __name__=="__main__":
    # Launch the server
    # Use pydbus to establish a session gdbus. Rather than system gdbus
    # TODO: Use try/except, etc. in case bus already exists. e.g. bus.get(BUS)
    bus = SessionBus()
    bus.publish(BUS, DBusService())

    # Start the repeating timer. It auto-starts, no need of rt.start()
    # RepeatedTimer(period between function calls, function())
    rt = RepeatedTimer(period, timer_event)

    # Enable R-Pi channel to perform callbacks on detection of a pulse.
    if not simulated_pulse:
        #GPIO.add_event_detect(channel, GPIO.RISING, callback=pulse_callback, 
        #                      bouncetime=1)
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=pulse_callback, 
                              bouncetime=1)
    print("server running...")
    try:
        loop.run()
    except KeyboardInterrupt:
        print("\nStopping timer...")
        rt.stop()
        raise
    finally:
        print("Stopping loop...")       
        loop.quit()
        sys.exit("Exiting...")
    # TODO: Test this Ctrl C exiting works corrrectly. May leave bus published?


