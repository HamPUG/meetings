#!/usr/bin/env python3
# presentation_4.py
#
# 1 .Minimum window
# 2. Provide a title <-- Not recommended. Probably be deprecated.
# 2. Set size request to make it bigger
# 2. Use dir to get the Window (self) attributes.
# 3. Add the title field when instantiating the Window.
# 4. Add a grid
# 4. Place a label in the grid
# 4. Place a frame in the grid

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gtk Presentation # 4")        
        self.set_size_request(600, 400)
        #print(dir(self))
        # 4. Provide a Grid container for the Window.
        self.grid = Gtk.Grid()
        self.add(self.grid)
           
        # 4. Add a label to the main grid
        self.label = Gtk.Label(label="My Label")
        self.grid.attach(self.label, 0, 0, 1, 1)        
        
        # 4. Add a Frame to the main grid
        self.frame = Gtk.Frame(label="A Frame")
        self.grid.attach(self.frame, 0, 1, 1, 1)
        
        
if __name__=="__main__":
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
	
