#!/usr/bin/env python3
#!
# Glade/Builder mixed with Gtk.Window.
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

glade_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.38.1 -->
<interface>
  <requires lib="gtk+" version="3.24"/>
  <object class="GtkHeaderBar" id="header_1">
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <property name="title" translatable="yes">Header Bar Glade Example</property>
    <property name="subtitle" translatable="yes">XML file was: header_1.glade</property>
    <property name="show-close-button">True</property>
    <child>
      <object class="GtkButton" id="button_1">
        <property name="label">gtk-file</property>
        <property name="visible">True</property>
        <property name="can-focus">True</property>
        <property name="receives-default">True</property>
        <property name="use-stock">True</property>
        <!--property name="use-icon">True</property-->
        <signal name="clicked" handler="cb_button_1" swapped="no"/>
      </object>
    </child>
  </object>
</interface>
"""


class ExampleWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Menu Example")
        self.set_default_size(500, 200)

        # Use Builder to read embedded xml string defining HeaderBar
        builder = Gtk.Builder()
        builder.add_from_string(glade_xml) 
        header = builder.get_object("header_1")
        builder.connect_signals(self)
        self.set_titlebar(header)
        
        # Add widgets using traditional method to the Gtk.Window
        self.grid = Gtk.Grid()
        self.grid.set_border_width(10)
        self.label = Gtk.Label(label="This is a label")
        self.grid.attach(self.label, 0,0,1,1)
        self.add(self.grid)

    def cb_button_1(self,button):
        self.label.set_text(self.label.get_text() + 
                            "\nButton 1 on HeaderBar clicked")

win = ExampleWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

