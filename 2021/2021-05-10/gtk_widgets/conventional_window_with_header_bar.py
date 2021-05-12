#!/usr/bin/env python3
#!
# Conventional Gtk.Window with header bar
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ExampleWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Conventional Gtk Window")
        self.set_default_size(400, 200)
        
        # Add a header to replace the title bar
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "HeaderBar Example"
        header_bar.props.subtitle = "conventional_window_with_header_bar.py"
        self.set_titlebar(header_bar)        
        
        # Create widgets and add to the Gtk.Window
        self.grid = Gtk.Grid()
        self.grid.set_border_width(20)       
        self.label = Gtk.Label(label="This is a label")
        self.grid.attach(self.label, 0,0,1,1)
        self.add(self.grid)

win = ExampleWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

