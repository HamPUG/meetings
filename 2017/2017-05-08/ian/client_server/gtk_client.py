#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# gtk_client.py
# A Gtk GUI client the retieves data over the gdbus using pydbus python module.
# Able to control the server.
# Set PROJECTOR = True for larger font size if presenting this application.
#
# Ian Stewart
# 2019-05-06
# If you give a man a stream of pulses and a clock ...he will go mad!
#
# TODO: Add message to go to Notifications
# TODO: Reset BUS to be 0.
# TODO: Use the Server Buttons.
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
    print("Please install pydbus: $ sudo pip3 install pydbus")
    print("Installation into: ~/.local/lib/python3.x/site-packages/pydbus")
    sys.exit("Exiting...")

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Pango
import time
# Variables / Constants...
#loop = GLib.MainLoop()
loop = Gtk.main
BUS = "org.freedesktop.velocity.server5"
INTERVAL_MS = 1000
TITLE = "Dash Panel Client"
DIVISOR = 10  # Use divisor to scale the progress bars. 
# With video_projector set to True, then Gtk will use a larger font.
PROJECTOR = True
PROJECTOR_FONT = "FreeSans, 15"
# Frame labels.
FRAME_1 = "Instantaneous Distance and Speed"
FRAME_2 = "Total Distance / Average Speed"
FRAME_3 = "Running Average"
FRAME_4 = "Controls"
FRAME_5 = "Server Controls"
# Frame1 Labels
F1_LABEL_1 = "Distance (m):"
F1_LABEL_2 = "Speed (m/s):"
F1_LABEL_3 = "Speed (km/h):"
F1_LABEL_4 = "Period (secs)"
F1_LABEL_5 = "Rotations (int)"
# Frame2 Labels
F2_LABEL_1 = "Distance (m):"
F2_LABEL_2 = "Distance (km):"
F2_LABEL_3 = "Speed (m/s):"
F2_LABEL_4 = "Speed (km/h):"
F2_LABEL_5 = "Duration (secs):"
F2_LABEL_6 = "Duration (h:m:s):"
# Frame3 Labels
F3_LABEL_1 = "Distance (m):"
F3_LABEL_2 = "Speed (m/s):"
F3_LABEL_3 = "Speed (km/h):"
F3_LABEL_4 = "Samples:"
# Frame4 Buttons
F4_BUTTON_1 = "Start"
F4_BUTTON_2 = "Stop"
F4_BUTTON_3 = "Reset"
F4_BUTTON_4 = "Exit"
# Frame4 Buttons
F5_BUTTON_1 = "Notify"
F5_BUTTON_2 = "B2"
F5_BUTTON_3 = "B3"
F5_BUTTON_4 = "B4"

# Display Version information.
print("Python:{}, Gtk:{}.{}.{}, GLib:{}.{}.{}, Pango:{}, pydbus:0.6.0" 
    .format(
    sys.version.split(" ")[0],
    Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION,
    GLib.MAJOR_VERSION, GLib.MINOR_VERSION, GLib.MICRO_VERSION,
    Pango.version_string())
    )


class MainWindow(Gtk.Window):
    """
    Launch Gtk GUI client. Connect to server. 
    """
    def __init__(self):
        Gtk.Window.__init__(self, title=TITLE)
        #self.set_default_size(150, 100)
        grid_main = Gtk.Grid()
        self.add(grid_main)

        # Modify the overall font name and size, for use with video projection.
        if PROJECTOR:  
            pangoFont = Pango.FontDescription(PROJECTOR_FONT)
            self.modify_font(pangoFont)

        # Get the session dbus
        bus = SessionBus()
        # Get the object
        try:
            self.server_1_object = bus.get(BUS)
        except GLib.Error as e:
            print("GLib.Error: {}.\nIs the server running?".format(BUS))
            #print(e)
            sys.exit("Exiting...")

        except GDBus.Error as e:
            # Doesn't seem to have GDBus.Error as an error.
            # TODO: Remove is never detected
            print("Error 2")
            print(e)
        # TODO: Check if it can hang here. If bus not registered / available? 

        # Create Frames to group different data in.
        frame_1 = Gtk.Frame(label=FRAME_1, margin=10)
        grid_main.attach(frame_1, 0, 0, 1, 1)
        frame_2 = Gtk.Frame(label=FRAME_2, margin=10)
        grid_main.attach(frame_2, 1, 0, 1, 1)
        frame_3 = Gtk.Frame(label=FRAME_3, margin=10)
        grid_main.attach(frame_3, 0, 1, 1, 2)
        frame_4 = Gtk.Frame(label=FRAME_4, margin=10)
        grid_main.attach(frame_4, 1, 1, 1, 1)
        frame_5 = Gtk.Frame(label=FRAME_4, margin=10)
        grid_main.attach(frame_5, 1, 2, 1, 1)

        # Frame_1 Grid for widgets  
        grid_frame_1 = Gtk.Grid()
        frame_1.add(grid_frame_1)
        # Frame_1 Static labels. xalign float from 0 = left to 1 = right
        f1_label_1 = Gtk.Label(F1_LABEL_1, margin=10, xalign=1)
        f1_label_2 = Gtk.Label(F1_LABEL_2, margin=10, xalign=1)
        f1_label_3 = Gtk.Label(F1_LABEL_3, margin=10, xalign=1)
        f1_label_4 = Gtk.Label(F1_LABEL_4, margin=10, xalign=1)
        f1_label_5 = Gtk.Label(F1_LABEL_5, margin=10, xalign=1)
        # Frame_1 Attach to grid
        grid_frame_1.attach(f1_label_1, 0, 0, 1, 1,)
        grid_frame_1.attach(f1_label_2, 0, 1, 1, 1,)
        grid_frame_1.attach(f1_label_3, 0, 2, 1, 1,)
        grid_frame_1.attach(f1_label_4, 0, 3, 1, 1,)
        grid_frame_1.attach(f1_label_5, 0, 4, 1, 1,)
        # Frame_1 Dynamic labels. Provide self. 
        # So they can be updated by any method.
        self.f1_label_1a = Gtk.Label("0", margin=10, xalign=1)
        self.f1_label_2a = Gtk.Label("0", margin=10, xalign=1)
        self.f1_label_3a = Gtk.Label("0", margin=10, xalign=1)
        self.f1_label_4a = Gtk.Label("0", margin=10, xalign=1)
        self.f1_label_5a = Gtk.Label("0", margin=10, xalign=1)
        # Frame_1 Attach to grid
        grid_frame_1.attach(self.f1_label_1a, 1, 0, 1, 1,)
        grid_frame_1.attach(self.f1_label_2a, 1, 1, 1, 1,)
        grid_frame_1.attach(self.f1_label_3a, 1, 2, 1, 1,)
        grid_frame_1.attach(self.f1_label_4a, 1, 3, 1, 1,)
        grid_frame_1.attach(self.f1_label_5a, 1, 4, 1, 1,)
        # Frame_1 Progress bar
        self.f1_progressbar_1 = Gtk.ProgressBar()
        grid_frame_1.attach(self.f1_progressbar_1, 2, 0, 1, 1,)
        self.f1_progressbar_1.set_fraction(0)

        # Frame_2 Grid for widgets 
        grid_frame_2 = Gtk.Grid()
        frame_2.add(grid_frame_2)
        # Frame_2 Static labels.
        f2_label_1 = Gtk.Label(F2_LABEL_1, margin=10, xalign=1)
        f2_label_2 = Gtk.Label(F2_LABEL_2, margin=10, xalign=1)
        f2_label_3 = Gtk.Label(F2_LABEL_3, margin=10, xalign=1)
        f2_label_4 = Gtk.Label(F2_LABEL_4, margin=10, xalign=1)
        f2_label_5 = Gtk.Label(F2_LABEL_5, margin=10, xalign=1)
        f2_label_6 = Gtk.Label(F2_LABEL_6, margin=10, xalign=1)
        # Frame_2 Attach to grid
        grid_frame_2.attach(f2_label_1, 0, 0, 1, 1,)
        grid_frame_2.attach(f2_label_2, 0, 1, 1, 1,)
        grid_frame_2.attach(f2_label_3, 0, 2, 1, 1,)
        grid_frame_2.attach(f2_label_4, 0, 3, 1, 1,)
        grid_frame_2.attach(f2_label_5, 0, 4, 1, 1,)
        grid_frame_2.attach(f2_label_6, 0, 5, 1, 1,)
        # Frame_2 Dynamic labels.
        self.f2_label_1a = Gtk.Label("0", margin=10, xalign=1)
        self.f2_label_2a = Gtk.Label("0", margin=10, xalign=1)
        self.f2_label_3a = Gtk.Label("0", margin=10, xalign=1)
        self.f2_label_4a = Gtk.Label("0", margin=10, xalign=1)
        self.f2_label_5a = Gtk.Label("0", margin=10, xalign=1)
        self.f2_label_6a = Gtk.Label("0", margin=10, xalign=1)
        # Frame_2 Attach to grid
        grid_frame_2.attach(self.f2_label_1a, 1, 0, 1, 1,)
        grid_frame_2.attach(self.f2_label_2a, 1, 1, 1, 1,)
        grid_frame_2.attach(self.f2_label_3a, 1, 2, 1, 1,)
        grid_frame_2.attach(self.f2_label_4a, 1, 3, 1, 1,)
        grid_frame_2.attach(self.f2_label_5a, 1, 4, 1, 1,)
        grid_frame_2.attach(self.f2_label_6a, 1, 5, 1, 1,)

        # Frame_3 Grid for widgets
        grid_frame_3 = Gtk.Grid()
        frame_3.add(grid_frame_3)
        # Frame_3 Static labels.
        f3_label_1 = Gtk.Label(F3_LABEL_1, margin=10, xalign=1)
        f3_label_2 = Gtk.Label(F3_LABEL_2, margin=10, xalign=1)
        f3_label_3 = Gtk.Label(F3_LABEL_3, margin=10, xalign=1)
        f3_label_4 = Gtk.Label(F3_LABEL_4, margin=10, xalign=1)
        # Frame_3 Attach to grid
        grid_frame_3.attach(f3_label_1, 0, 0, 1, 1,)
        grid_frame_3.attach(f3_label_2, 0, 1, 1, 1,)
        grid_frame_3.attach(f3_label_3, 0, 2, 1, 1,)
        grid_frame_3.attach(f3_label_4, 0, 3, 1, 1,)
        # Frame_3 Dynamic labels.
        self.f3_label_1a = Gtk.Label("0", margin=10, xalign=1)
        self.f3_label_2a = Gtk.Label("0", margin=10, xalign=1)
        self.f3_label_3a = Gtk.Label("0", margin=10, xalign=1)
        self.f3_label_4a = Gtk.Label("0", margin=10, xalign=1)
        # Frame_3 Attach to grid
        grid_frame_3.attach(self.f3_label_1a, 1, 0, 1, 1,)
        grid_frame_3.attach(self.f3_label_2a, 1, 1, 1, 1,)
        grid_frame_3.attach(self.f3_label_3a, 1, 2, 1, 1,)
        grid_frame_3.attach(self.f3_label_4a, 1, 3, 1, 1,)
        # Frame_3 Progress bar.
        self.f3_progressbar_1 = Gtk.ProgressBar()
        grid_frame_3.attach(self.f3_progressbar_1, 2, 0, 1, 1,)
        self.f3_progressbar_1.set_fraction(0)

        # Frame_4 Grid for widgets
        grid_frame_4 = Gtk.Grid()
        frame_4.add(grid_frame_4)
        # Frame_4 Buttons. Start/Stop/Reset buttons.
        self.f4_button_1 = Gtk.Button(label=F4_BUTTON_1, margin=10)
        self.f4_button_2 = Gtk.Button(label=F4_BUTTON_2, margin=10)
        self.f4_button_2.set_sensitive(False)
        self.f4_button_3 = Gtk.Button(label=F4_BUTTON_3, margin=10)
        self.f4_button_4 = Gtk.Button(label=F4_BUTTON_4, margin=10)
        # Frame_4 Button call-back signals
        self.f4_button_1.connect("clicked", self.cb_f4_button_1,
                                 self.f4_button_2) 
        self.f4_button_2.connect("clicked", self.cb_f4_button_2, 
                                 self.f4_button_1)
        self.f4_button_3.connect("clicked", self.cb_f4_button_3)
        self.f4_button_4.connect("clicked", self.cb_f4_button_4)
        # Frame_4 Attach to grid
        grid_frame_4.attach(self.f4_button_1, 0, 0, 1, 1, )
        grid_frame_4.attach(self.f4_button_2, 1, 0, 1, 1, )
        grid_frame_4.attach(self.f4_button_3, 2, 0, 1, 1, )
        grid_frame_4.attach(self.f4_button_4, 3, 0, 1, 1, )


        # Frame_5 Grid for widgets
        grid_frame_5 = Gtk.Grid()
        frame_5.add(grid_frame_5)
        # Frame_5 Buttons. Start/Stop/Reset buttons.
        self.f5_button_1 = Gtk.Button(label=F5_BUTTON_1, margin=10)
        self.f5_button_2 = Gtk.Button(label=F5_BUTTON_2, margin=10)
        self.f5_button_3 = Gtk.Button(label=F5_BUTTON_3, margin=10)
        self.f5_button_4 = Gtk.Button(label=F5_BUTTON_4, margin=10)
        # Frame_5 Button call-back signals
        self.f5_button_1.connect("clicked", self.cb_f5_button_1)
        self.f5_button_2.connect("clicked", self.cb_f5_button_2)
        self.f5_button_3.connect("clicked", self.cb_f5_button_3)
        self.f5_button_4.connect("clicked", self.cb_f5_button_4)
        # Frame_5 Attach to grid
        grid_frame_5.attach(self.f5_button_1, 0, 0, 1, 1, )
        grid_frame_5.attach(self.f5_button_2, 1, 0, 1, 1, )
        grid_frame_5.attach(self.f5_button_3, 2, 0, 1, 1, )
        grid_frame_5.attach(self.f5_button_4, 3, 0, 1, 1, )

        # Launch with client started...
        self.cb_f4_button_1(self.f4_button_1, self.f4_button_2)

    def cb_f4_button_1(self, button_start, button_stop):
        """ 
        Start button clicked. Disable Start and enable Stop. 
        Start the timer, while monitoring the sensitive of the Start button.
        """
        button_start.set_sensitive(False)
        button_stop.set_sensitive(True)
        GLib.timeout_add(INTERVAL_MS, self.event_timer, button_start)

    def cb_f4_button_2(self, button_stop, button_start):
        """ 
        Stop button clicked. Disable Stop and enable Start 
        """
        button_stop.set_sensitive(False)
        button_start.set_sensitive(True)

    def cb_f4_button_3(self, button):
        """ 
        Reset all the labels to zero. 
        Pass command to server to run refresh method to set counter to zero.
        """        
        self.server_1_object.refresh()

        self.f1_label_1a.set_label("")
        self.f1_label_2a.set_label("")
        self.f1_label_3a.set_label("")
        self.f1_label_4a.set_label("")
        self.f1_label_5a.set_label("")
        self.f2_label_1a.set_label("")
        self.f2_label_2a.set_label("")
        self.f2_label_3a.set_label("")
        self.f2_label_4a.set_label("")
        self.f2_label_5a.set_label("")
        self.f2_label_6a.set_label("")
        self.f2_label_5a.set_label("")
        self.f2_label_6a.set_label("")
        self.f3_label_1a.set_label("")
        self.f3_label_2a.set_label("")
        self.f3_label_3a.set_label("")
        self.f3_label_4a.set_label("")

    def cb_f4_button_4(self, button):
        """ 
        Exit. But server keeps running
        """
        # TODO: Fix this. client shutdown and Server shutdown.
        #loop.quit
        win.connect("destroy", Gtk.main_quit)
        Gtk.main_quit()
        print("Gtk quit")
        # Send command to shut down the server. 
        self.server_1_object.quit()
        print("Server quit")
        sys.exit()

    def event_timer(self, button_start): 
        """
        Event timer. Based on Start button is_sensitive determines Start/Stop.
        Call to method to retrieve the server and update the labels.
        """
        self.retrieve_from_server()
        if button_start.is_sensitive():
            return False
        else:
            return True

    def retrieve_from_server(self):
        """
        get_status performed on server returns a message list of string data.
        Update the labels with the new data.
        """
        reply = self.server_1_object.get_status()
        #print(reply) # message_list from server
        # ['15', '1', '14.5', '14.5', '52.2', '15', '0days-00:00:15', '153.2',
        # '0.2', '9.6', '34.5', '5.50', '5.5', '19.8', '4']
        #print(", ".join(reply)) # Print as a comma, space seperated string 
        # Frame_1 labels update        
        self.f1_label_1a.set_label(reply[2])
        self.f1_label_2a.set_label(reply[3])
        self.f1_label_3a.set_label(reply[4])
        self.f1_label_4a.set_label(reply[1])
        self.f1_label_5a.set_label(reply[0])
        # Frame_1 Progress bar update.
        self.f1_progressbar_1.set_fraction(float(reply[2])/DIVISOR)
        # Frame_2 labels update
        self.f2_label_1a.set_label(reply[7])
        self.f2_label_2a.set_label(reply[8])
        self.f2_label_3a.set_label(reply[9])
        self.f2_label_4a.set_label(reply[10])
        self.f2_label_5a.set_label(reply[5])
        self.f2_label_6a.set_label(reply[6])
        # Frame_3 labels update
        self.f3_label_1a.set_label(reply[11])
        self.f3_label_2a.set_label(reply[12])
        self.f3_label_3a.set_label(reply[13])
        self.f3_label_4a.set_label(reply[14])
        # Frame_1 Progress bar update.
        self.f3_progressbar_1.set_fraction(float(reply[11])/DIVISOR)
        
        # TODO: Replace Start/Stop buttons with a single toggle button. E.g.
        #  button = Gtk.ToggleButton("Button 1")
        #    def on_button_toggled(self, button, name):
        #        if button.get_active():
        #            state = "on"
        #        else:
        #            state = "off"
        #        print("Button", name, "was turned", state)

    def cb_f5_button_1(self, button):
        print("button f5_1")
        self.server_1_object.info()

    def cb_f5_button_2(self, button):
        print("button f5_2")
    def cb_f5_button_3(self, button):
        print("button f5_3")
    def cb_f5_button_4(self, button):
        print("button f5_4")


if __name__=="__main__":
    # Launch Client GUI application.
    win = MainWindow()
    # TODO: What's the difference for Gtk. delete-event or destroy?
    #win.connect("delete-event", Gtk.main_quit)
    win.connect("destroy", Gtk.main_quit) #GLib.MainLoop.quit) # Gtk.main_quit)
    win.show_all()
    # Run the  Gtk.main or GLib.MainLoop loop.
    # Gtk.main prevents Ctrl C or Ctrl Z.  
    # requires clicking on Exit button of icon.
    # GLib.MainLoop. Ctrl C crashes outof the application.
    loop()
    #loop.run() # <-- For GLib

    # GLib.MainLoop.quit
    # TypeError: argument self: Expected GLib.MainLoop, 
    # but got __main__.MainWindow


