#!/usr/bein./env python3
#
# get_module_classes_constants.py
#
# A utility program designed to review the output of a dir() of a module and
# acquire the Classes (in camel case) and the constants or flags (in uppercase).
# Constants are acquired with one level of nesting.
# For example the Gtk module has:
#   Gtk.MAJOR_VERSION. An integer constant with a value of 3.
# It also has the following nested in classes
#   Gtk.ButtonsType.OK_CANCEL
#   Gtk.DialogFlags.MODAL
#   Gtk.WindowPosition.MOUSE
#
# Output to the console may include informational messages, like:
# PyGIDeprecationWarning: GLib.IO_FLAG_MASK is deprecated; use GLib.IOFlags.MASK instead
# PyGIDeprecationWarning: GObject.G_MAXINT64 is deprecated; use GLib.MAXINT64 instead
#
# Constants starting with an integer are rejected by python
# Error. Class: GLib.SpawnError, Attribute: 2BIG
# Error. Class: Gdk.EventType, Attribute: 2BUTTON_PRESS
#
# The output is two csv files written to the current working directory.
# One for listing classes the other for constants/flags/enums.
#
# Ian Stewart
# 2020-06-28
# TODO: Make a GUI version and use a treeview
#
import sys
import os

#=====NOTE=====
#
# Change the modules that are imported and the items in the 'module_list'

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gst, GObject, Gtk, Gdk, GLib

#module_list = ["Gtk", "GObject", "Gst", "Gdk", "GLib"]
module_list = ["Gtk"]
#module_list = ["sys", "os"]

#=====


def check_for_sub_class(module):
    """
    A class may have a sub-class and it may have constants. For example:
    GObject.Signal has the sub-class BoundSignal. However BoundSignal has no
    constants.
    """
    module_list = dir(eval(module))
    print("\n#==========")
    print("\nPython Module: {}. Total top level attributes: {}."
                    .format(module, len(module_list)))
    #print(module_list)
    #sys.exit()

    # Get classes. Start with capital letter, but not all capitals.
    constant_list = []
    class_list = []
    for attribute in module_list:
        if attribute.isupper():
            type_string = str(type(eval(module + "." + attribute))) 
            value_string = str(eval(module + "." + attribute)) 
            constant_list.append(module + "." + attribute + "," 
                            + type_string + "," + value_string)
            continue
        if attribute[0].isupper():
            class_list.append(module + "." + attribute)
            
    #print(class_list)
    #sys.exit()
       
    # For each class, get constants, and see if they contain sub-classes
    sub_class_list = []
    for class_item in class_list:

        try:        
            # The dir() may be of a deprecated class, and a warning may be issued.
            temp_list = dir(eval(class_item))
            for attribute in temp_list:
                if attribute.isupper():
                    type_string = str(type(eval(class_item + "." + attribute)))
                    value_string = str(eval(class_item + "." + attribute)) 
                    constant_list.append(class_item + "." + attribute + "," 
                                    + type_string + "," + value_string)
                    continue
                if attribute[0].isupper():
                    sub_class_list.append(class_item + "." + attribute)  
        except:
            # Error with constants beginning with an integer. 
            # E.g. Gdk.EventType.2BUTTON_PRESS
            print("Error. Class: {}, Attribute: {}".format(class_item, attribute))          

    print("\nAnalysis of module: {}".format(module))
    print("Total of all Upper Case ~ Constants & Flags:", len(constant_list))       
    #print(constant_list)
 
    print("Total of all Classes:", len(class_list))       
    #print(class_list)   
    
    if len(sub_class_list) > 0:
        print("\nWarning: Classes may contain classes which may contain constants.")
        print("Manually check and class within a class.")     
        print("Number of classes within a class:", len(sub_class_list))
        print("List of sub-classes:")
        for item in sub_class_list:
            print(item)
        print("")
    
    
    # Create csv files:
    filename_1 = module + "_class.csv"
    filename_2 = module + "_constant.csv"

    with open(filename_1, "w") as fout:
        for class_item in class_list:
            fout.write(class_item + "\n")
            
    with open(filename_2, "w") as fout:
        for constant_item in constant_list:
            fout.write(constant_item + "\n")

    print("Data written to files: {} and {}".format(filename_1, filename_2)) 
                                      
    return class_list, constant_list


if __name__ == "__main__":
    
    for module in module_list:
        class_list, constant_list = check_for_sub_class(module)    
        print("Total items in returned lists. Class: {}, Constant: {}"
                .format(len(class_list), len(constant_list)))

    #TODO: These returned list may be processed further.

sys.exit()


"""
Example of class in a class. They need to be manually checked.
However in these cases they didn't have any constants...

>>> dir(Gtk.Template.Callback)
['__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', 
'__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', 
'__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', 
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
'__sizeof__', '__str__', '__subclasshook__', '__weakref__']

>>> dir(Gtk.Template.Child)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', 
'__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', 
'__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', 
'__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
'__str__', '__subclasshook__', '__weakref__']


"""

