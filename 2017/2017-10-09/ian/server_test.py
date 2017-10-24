#!/usr/bin/env python3
#!
# server_test.py
# Publish a string of data every second onto the System D-Bus
# To check server is emitting data OK use the gdbus utility command...
# $ gdbus monitor --system --dest org.example.ca.server

# Importing
import asyncio
import random
from pydbus import SystemBus
from pydbus.generic import signal

# Instantiation / Variables / Constants 
iface_name = "org.example.ca.server"
# Note that server uses the System D-Bus (not Session D-Bus)
bus = SystemBus()
# Main event loop
loop = asyncio.get_event_loop()


class Server_XML(object):
    """
    Server_XML definition. 
    type='i' for integer, type='d' for double/float, type='s' for string 
    type='ai' for list of 32-bit signed integers, type='as' for string list
    """
    dbus = """
    <node>
        <interface name="org.example.ca.server">
            <signal name="app_signal">
                <arg type='s'/>
            </signal>
        </interface>
    </node>
    """
    app_signal = signal()


async def emit_random_number():
    "Emit a message every second with random integer between 0 and 100."
    while True:
        x = random.randrange(100)
        message = "The random integer for this second is {}".format(x)
        print("Server:", message)
        emit.app_signal(message)
        await asyncio.sleep(1)


if __name__=="__main__":
    print("Server starting")
    # Setup server to emit signals over the DBus
    emit = Server_XML()
    bus.publish(iface_name, emit)
    # Add tasks
    loop.create_task(emit_random_number())
    loop.run_forever()

'''
Example of running the server...

$ python3 server_test.py
Server starting
Server: The random integer for this second is 45
Server: The random integer for this second is 11
Server: The random integer for this second is 19

Example: Using gdbus to check server program is emitting OK...

$ gdbus monitor --system --dest org.example.ca.server
Monitoring signals from all objects owned by org.example.ca.server
The name org.example.ca.server is owned by :1.1823
/org/example/ca/server: org.example.ca.server.app_signal ('The random integer for this second is 45',)
/org/example/ca/server: org.example.ca.server.app_signal ('The random integer for this second is 11',)

'''
