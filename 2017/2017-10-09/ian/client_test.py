#!/usr/bin/env python3
#!
# client_test.py
# Client monitors for server applications System D-Bus signal emissions.
# Client is a command line application.
# GLib.MainLoop is used to provide the loop
# TODO: Change code to use asyncio loop?
# To Demo:
# From one console terminal launch server_test.py
# From another console terminal launch client_test.py

import sys
from gi.repository import GLib
from pydbus import SystemBus

# Instantiation / Variables / Constants
# Note that server uses the System D-Bus (not Session D-Bus)
iface_name = "org.example.ca.server"
bus = SystemBus()
loop = GLib.MainLoop()

bus_name = "org.example.ca.server"
dbus_filter = "/" + "/".join(bus_name.split("."))
# print(dbus_filter) # /org/example/ca/server


def cb_server_signal_emission(*args):
    """
    Callback on emitting signal from server
    Emitted signal is the value of the counter
    Data is in args[4]. The first item in a tuple.args[4][0]
    """
    data = args[4][0]
    print("Client:", data)


if __name__=="__main__":
    print("Client Starting...")
    # Subscribe to bus to monitor for server signal emissions
    # dbus_filter. E.g. /org/example/ca/server
    bus.subscribe(object = dbus_filter, 
                  signal_fired = cb_server_signal_emission)
    loop.run()

'''
Example of client_test.py...

$ python3 client_test.py
Client Starting...
Client: The random integer for this second is 12
Client: The random integer for this second is 98
Client: The random integer for this second is 6
'''
