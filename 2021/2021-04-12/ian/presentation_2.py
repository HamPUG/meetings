#!/usr/bin/env python3
# presentation_2.py
#
# 1. Minimum window
# 2. Provide a title
# 2. Set size request to make it bigger
# 2. Use dir() to display attributes of self.


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        
        # 2. Title, window size, and dir()
        self.set_title("Gtk Presentation # 2")
        
        self.set_size_request(600, 400)
        
        print(dir(self))        
        
        
if __name__=="__main__":
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
	
