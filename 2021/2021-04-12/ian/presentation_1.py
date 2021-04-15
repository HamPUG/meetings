#!/usr/bin/env python3
# presentation_1.py
#
# 1. Minimum window. Can not read all the supplied title.





import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)


if __name__=="__main__":	
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
	
