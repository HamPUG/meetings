#!/usr/bin/env python
#
# Program: pyudev_demo_3.py
# Author: Ian Stewart
# Date: 2015-Nov-09
# Tab = 4 x spaces
#
# Objective: Demonstrate pyudev detecting removal and insertion of USB device
# A wx toolkit window is created and wx MainLoop() maintains the window.
# pyudev monitors for events and provides a call-back to a function which
# recieves the event object. pyudev is a binding to libudev.
#
# Pre-requisites:
# python-wxgtk2.8 --> $ sudo apt-get install python-wxgtk2.8
# wxpython --> $ sudo pip install wxpython
# pyudev --> $ sudo pip install pyudev
#
# References:
# http://pyudev.readthedocs.org/en/latest/api/pyudev.wx.html
# http://pyudev.readthedocs.org/en/latest/api/pyudev.html
# https://github.com/pyudev/pyudev/tree/develop/tests
MESSAGE_1 = '''pyudev demo #3'''
MESSAGE_2 = '''Insert and Remove USB device. 
Observe the stdout on the terminal.

Demo #3 is:
Filtering
'''
import sys
from pyudev import Context, Monitor
from pyudev.wx import MonitorObserver, EVT_DEVICE_EVENT
try:
    import wx 
except ImportError:
    sys.exit("ImportError: No module named 'wx'")

def device_event(event):
    '''Callback for a change in a USB device'''

    print('Event Action: {0.device.action}\n'
          'Device Path: {0.device.device_path}'.format(event))

if __name__ == "__main__":
    # Create a wx.GUI window with text.
    app = wx.App()
    frame = wx.Frame(None, -1, MESSAGE_1, size=(350,150))
    panel = wx.Panel(frame)
    sizer = wx.GridBagSizer(5, 5)
    text1 = wx.TextCtrl(panel, pos=(3, 3), size=(320, 130), style=wx.TE_MULTILINE)
    text1.AppendText(MESSAGE_2)
    sizer.Add(text1, pos=(0, 1), span=(1, 5), flag=wx.TOP|wx.EXPAND, border=5)
    panel.SetSizer(sizer)
    frame.Show()

    # Establish the monitoring and callback to the function device_event()
    context = Context()
    #Create a monitor by connecting to the kernel daemon through netlink
    monitor = Monitor.from_netlink(context, source=u'udev')

    # Filtering
    monitor.filter_by(subsystem='input')

    observer = MonitorObserver(monitor)

    observer.Bind(EVT_DEVICE_EVENT, device_event)
    monitor.start()

    # Use the wx loop
    app.MainLoop()

'''
Notes: 

A Monitor objects connects to the udev daemon and listens for changes to the device list. A monitor is created by connecting to the kernel daemon through netlink (see from_netlink()):

classmethod from_netlink(context, source=u'udev')
Create a monitor by connecting to the kernel daemon through netlink.


Once the monitor is created, you can add a filter using filter_by() or filter_by_tag() to drop incoming events in subsystems, which are not of interest to the application:

monitor events asynchronously with MonitorObserver



Check versions:

import wx
>>> wx.version()
'2.8.12.1 (gtk2-unicode)'

>>> import pyudev
>>> pyudev.udev_version()
219
>>> pyudev.__version__
u'0.17'
>>> pyudev.__version_info__
(0, 17)
>>> 

$ sudo apt-get install python-wxgtk2.8
Reading package lists... Done
Building dependency tree       
Reading state information... Done
python-wxgtk2.8 is already the newest version.
python-wxgtk2.8 set to manually installed.
0 upgraded, 0 newly installed, 0 to remove and 26 not upgraded.
$ 

===

print(dir(event))

['ClassName', 'Clone', 'Destroy', 'EventObject', 'EventType', 'GetClassName', 'GetEventObject', 'GetEventType', 'GetId', 'GetSkipped', 'GetTimestamp', 'Id', 'IsCommandEvent', 'IsSameAs', 'ResumePropagation', 'SetEventObject', 'SetEventType', 'SetId', 'SetTimestamp', 'ShouldPropagate', 'Skip', 'Skipped', 'StopPropagation', 'Timestamp', 

'_GetSelf', '_SetSelf', '__class__', '__del__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__swig_destroy__', '__weakref__', 

'device', 'this', 'thisown']

===
print(dir(event.device))
['__abstractmethods__', '__class__', '__contains__', '__del__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__metaclass__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_abc_cache', '_abc_negative_cache', '_abc_negative_cache_version', '_abc_registry', '_as_parameter_', '_libudev', 'action', 'ancestors', 'asbool', 'asint', 'attributes', 'children', 'context', 'device_links', 'device_node', 'device_number', 'device_path', 'device_type', 'driver', 'find_parent', 'from_device_file', 'from_device_number', 'from_environment', 'from_name', 'from_path', 'from_sys_path', 'get', 'is_initialized', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'parent', 'sequence_number', 'subsystem', 'sys_name', 'sys_number', 'sys_path', 'tags', 'time_since_initialized', 'traverse', 'values']

===
print(dir(event.device.action))
event.device.action --> add, remove

['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getslice__', '__gt__', '__hash__', '__init__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_formatter_field_name_split', '_formatter_parser', 'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'index', 'isalnum', 'isalpha', 'isdecimal', 'isdigit', 'islower', 'isnumeric', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']

 dir(pyudev.wx)
['DeviceAddedEvent', 'DeviceChangedEvent', 'DeviceEvent', 'DeviceMovedEvent', 'DeviceRemovedEvent', 'EVT_DEVICE_ADDED', 'EVT_DEVICE_CHANGED', 'EVT_DEVICE_EVENT', 'EVT_DEVICE_MOVED', 'EVT_DEVICE_REMOVED', 'EvtHandler', 'MonitorObserver', 'NewEvent', 'PostEvent', 'WxUDevMonitorObserver', '__builtins__', '__doc__', '__file__', '__name__', '__package__', 'absolute_import', 'division', 'print_function', 'pyudev', 'unicode_literals']


'''
