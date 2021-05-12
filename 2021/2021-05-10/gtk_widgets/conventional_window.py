#!/usr/bin/env python3
#!
# Conventional Gtk.Window
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ExampleWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Conventional Gtk Window")
        self.set_default_size(400, 200)
        
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
