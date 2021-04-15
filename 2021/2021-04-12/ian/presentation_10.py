#!/usr/bin/env python3
# presentation_9.py
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
# 8. Add CSS function and call it on launching application.
# 8. set style context for label to use CSS 
# 9. Add CSS for Frame and buttons
# 10. Add CSS Colour to buttons and label

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def add_provider(widget):
    # Provide the CSS for labels and frames.
    screen = widget.get_screen()
    style = widget.get_style_context()
    provider = Gtk.CssProvider()
    provider.load_from_data("""
    /* 10 Add colours to label and buttons */
    .label_top {
        border: 1px solid #000000;
        margin: 15px;
        font: 30px Arial, sans-serif;
        background: SkyBlue;
        }   
             
    .frame_second {
        margin: 10px;
        font: 25px Courier New, monospace;
        } 

    .button_in_frame_grid {
        margin: 5px;
        font: 25px Arial, sans-serif;
        background: Yellow;
        }       
    """.encode('utf-8')) 
    style.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gtk Presentation # 9")        
        self.set_size_request(600, 400)
        #print(dir(self))

        # Provide grid for window and insert a frame into the grid.
        self.grid = Gtk.Grid()
        self.add(self.grid)   
        
        # Add a label and a frame to the main frame
        self.label = Gtk.Label(label="My Label")
        self.label.get_style_context().add_class("label_top")
        self.grid.attach(self.label, 0, 0, 1, 1)        
        self.frame = Gtk.Frame(label="A Frame")
        self.frame.get_style_context().add_class("frame_second") 
        self.frame.set_label_align(0.5,0.5)       
        self.grid.attach(self.frame, 0, 1, 1, 1)  
        
        # Provide a grid for the frame and add button array with callback
        self.frame_grid = Gtk.Grid()
        self.frame.add(self.frame_grid)
        self.button_list = []
        for i, name in enumerate(["B1", "B2", "B3", "B4"]):
            button = Gtk.Button(label=name)
            button.get_style_context().add_class("button_in_frame_grid")
            button.connect("clicked", self.on_button_clicked, i)
            self.button_list.append(button)
            self.frame_grid.attach(self.button_list[i], i, 0, 1, 1)
            
    def on_button_clicked(self, button, identifier):
        s = "Button #{}".format(identifier)
        self.label.set_label(s)
        
        
            
if __name__=="__main__":
    win = MyWindow()
    win.connect("realize", add_provider)    
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
	
