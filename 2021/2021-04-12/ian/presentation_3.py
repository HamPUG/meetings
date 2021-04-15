#!/usr/bin/env python3
# presentation_3.py
#
# 1 .Minimum window
# 2. Provide a title <-- Not recommended. Probably deprecated
# 2. Set size request to make it bigger
# 2. Use dir to get the Window (self) attributes.
# 3. Add the title field when instantiating the Window.

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
		
		# 3. title= included in instantiation
        Gtk.Window.__init__(self, title="Gtk Presentation # 3")        
        self.set_size_request(600, 400)
        #print(dir(self))
        
        
if __name__=="__main__":
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
	
