#!/usr/bin/env python3
# presentation_7.py
#
# 1 .Minimum window
# 2. Provide a title <-- Not recommended. Probably be deprecated.
# 2. Set size request to make it bigger
# 2. Use dir to get the Window (self) attributes.
# 3. Add the title field when instantiating the Window.
# 4. Add a grid
# 4. Place a frame in the grid
# 5. In the frame add another grid
# 5. Create a list of buttons and place them into the frames grid.
# 6. Add connect to each button to call routine
# 6. When buttons are clicked perform action to update label.
# 7. Add an identifier field to the buttons
# 7. On callback use identifier.

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gtk Presentation # 7")        
        self.set_size_request(600, 400)
        #print(dir(self))

        # Provide grid for window and insert a frame into the grid.
        self.grid = Gtk.Grid()
        self.add(self.grid)   
        
        # Add a label and a frame to the main frame
        self.label = Gtk.Label(label="My Label")
        self.grid.attach(self.label, 0, 0, 1, 1)        
        self.frame = Gtk.Frame(label="A Frame")
        self.grid.attach(self.frame, 0, 1, 1, 1)  
        
        # Provide a grid for the frame and add button array with callback
        self.frame_grid = Gtk.Grid()
        self.frame.add(self.frame_grid)
        self.button_list = []
        for i, name in enumerate(["B1", "B2", "B3", "B4"]):
            button = Gtk.Button(label=name)
            
            # 7. Add identifier "i"
            button.connect("clicked", self.on_button_clicked, i)
            
            self.button_list.append(button)
            self.frame_grid.attach(self.button_list[i], i, 0, 1, 1)
            
    def on_button_clicked(self, button, identifier):
        # 7. Update label with identifier
        s = "Button #{}".format(identifier)
        self.label.set_label(s)
        
        
            
if __name__=="__main__":
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
	