#!/usr/bin/env python3
#!
# Glade/Builder Gtk.Window.
# Conventional window with glade components related to HeaderBar.
# Includes signals to write dummy file, etc.
# Ian Stewart 2021-05-10

import time
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

TESTING = True

class Main_Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Menu Example")
        self.set_default_size(500, 200)
        # Path and filename of working file.
        self.filename = None
        self.main_data = "This is a test \nLine 2\n"

        # Use Builder to read embedded xml string defining HeaderBar
        self.builder = Gtk.Builder()
        self.builder.add_from_string(glade_xml)
        #self.builder.add_from_file("header_bar_4.glade")        
        self.header_bar = self.builder.get_object("headerbar")
        self.builder.connect_signals(self)
        self.set_titlebar(self.header_bar)

        self.header_bar.set_title("Header Bar Demo")
        self.header_bar.set_subtitle("2021-05-06")        
        
        # Add widgets using traditional method to the Gtk.Window
        self.grid = Gtk.Grid()
        self.grid.set_border_width(10)
        self.label = Gtk.Label(label="This is a label")

        self.grid.attach(self.label, 0,0,1,1)
        self.add(self.grid)


    # Callbacks on Main buttons in header bar
    def cb_open(self, button):
        """Open button on Header Bar. Sets self.filename variable"""
        print("Open File callback")
        dialog = Gtk.FileChooserDialog(
                title="Please choose a file", 
                parent=self, 
                action=Gtk.FileChooserAction.OPEN
                )
        dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
                )

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            self.filename = dialog.get_filename()
            if TESTING:
                # Testing. Place a time stamp into the file each time it is opened.
                # E.g. 'Fri May  7 16:46:41 2021'
                with open(self.filename, "a") as fout:
                    fout.write("Opened: " + time.ctime() + "\n")            
                
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()
        
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)  


    def cb_new(self, button):
        """Select a new file"""
        print("New File callback")
        self.cb_save_as(button)
        

    def cb_save(self, button):
        """Save button on Header Bar. Save unless variable not set."""
        print("Save File callback")

        if self.filename:
            with open(self.filename, "w") as fout:
                fout.write(self.main_data)
        else:
            # If self.flename is blank then call the Save_As method.
            self.cb_save_as(button)
        
        
    def cb_save_as(self, button):
        """Save_as button on Header Bar. Opens Dialog, sets variable, and saves"""
        print("Save_As File callback")        
        dialog = Gtk.FileChooserDialog(
                title="Please provide a file name", 
                parent=self, 
                action=Gtk.FileChooserAction.SAVE
                )
        dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE,
                Gtk.ResponseType.OK,
                )

        self.add_filters(dialog)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Save button clicked")
            print("File selected: " + dialog.get_filename())
            self.filename = dialog.get_filename()

            # Write main data to file
            with open(self.filename, "w") as fout:
                fout.write(self.main_data)            
                        
            if TESTING:
                # Testing. Place a time stamp into the file each time it is opened.
                # E.g. 'Fri May  7 16:46:41 2021'
                with open(self.filename, "a") as fout:
                    fout.write("Created: " + time.ctime() + "\n")             
            
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()


    # Callbacks for Popover main menu
    def cb_close(self, *args):
        """ Main close in Popover menu"""
        Gtk.main_quit()    
    
    
    def cb_something_1(self, button):
        """Modify to meet the needs of the application."""
        print("Do Something 1")  


    def cb_something_2(self, button):
        """Modify to meet the needs of the application."""
        print("Do Something 2")  


    def cb_something_3(self, button):
        """Modify to meet the needs of the application."""
        print("Do Something 3")  


    def cb_something_4(self, button):
        """Modify to meet the needs of the application."""        
        print("Do Something 4")  
     
       
    def cb_about_show(self, button):
        """Show the About dialog."""        
        print("About Dialog show")  
        self.about_dialog = self.builder.get_object("about_dialog")  
        self.about_dialog.show_all()
               
    # Callback in About Dialog           
    def cb_about_hide(self, *args):
        """About dialog. Response to Close button.""" 
        print("About Dialog hide")
        self.about_dialog.hide()

glade_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.38.1 

Glade - A user interface designer for GTK+ and GNOME.
Copyright (C) 2012-2018 Juan Pablo Ugarte

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

Author: Juan Pablo Ugarte

-->
<interface domain="glade">
  <requires lib="gtk+" version="3.20"/>
  <!-- interface-license-type lgplv2 -->
  <!-- interface-name Glade -->
  <!-- interface-description A user interface designer for GTK+ and GNOME. -->
  <!-- interface-copyright 2012-2018 Juan Pablo Ugarte -->
  <!-- interface-authors Juan Pablo Ugarte -->
  <object class="GtkAboutDialog" id="about_dialog">
    <property name="can-focus">False</property>
    <property name="border-width">5</property>
    <property name="resizable">False</property>
    <property name="modal">True</property>
    <property name="type-hint">dialog</property>
    <property name="copyright" translatable="yes">© 2021 Ian Stewart.
    </property>
    <property name="comments" translatable="yes">Gtk Header Bar</property>
    <property name="website">http://github.com/irsbugs/header-bar</property>
    <property name="website-label" translatable="yes">Source Code web site</property>
    <property name="authors">Ian Stewart &lt;stwrtn@gmail.com&gt;
    </property>
    <property name="logo">Icon-Gear02-Blue.svg</property>
    <property name="license-type">gpl-3-0</property>
    <signal name="response" handler="cb_about_hide" swapped="no"/>
    <child internal-child="vbox">
      <object class="GtkBox" id="aboutdialog-vbox1">
        <property name="can-focus">False</property>
        <property name="orientation">vertical</property>
        <property name="spacing">2</property>
        <child internal-child="action_area">
          <object class="GtkButtonBox" id="aboutdialog-action_area1">
            <property name="can-focus">False</property>
            <property name="layout-style">end</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="pack-type">end</property>
            <property name="position">0</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
  <object class="GtkPopoverMenu" id="main_menu">
    <property name="can-focus">False</property>
    <child>
      <object class="GtkBox">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <property name="border-width">4</property>
        <property name="orientation">vertical</property>
        <property name="spacing">2</property>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">Close Project</property>
            <signal name="clicked" handler="cb_close" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkSeparator">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">Do Something 1</property>
            <signal name="clicked" handler="cb_something_1" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">Do Something 2</property>
            <signal name="clicked" handler="cb_something_2" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">Do Something 3</property>
            <signal name="clicked" handler="cb_something_3" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">4</property>
          </packing>
        </child>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">Do Something 4</property>
            <signal name="clicked" handler="cb_something_4" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">5</property>
          </packing>
        </child>
        <child>
          <object class="GtkSeparator">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">6</property>
          </packing>
        </child>
        <child>
          <object class="GtkModelButton">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="text" translatable="yes">About</property>
            <signal name="clicked" handler="cb_about_show" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">7</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="submenu">main</property>
        <property name="position">1</property>
      </packing>
    </child>
  </object>
  <object class="GtkHeaderBar" id="headerbar">
    <property name="name">headerbar</property>
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <property name="show-close-button">True</property>
    <child>
      <object class="GtkMenuButton">
        <property name="name">menu-button</property>
        <property name="visible">True</property>
        <property name="can-focus">True</property>
        <property name="receives-default">True</property>
        <property name="tooltip-text" translatable="yes">Main Menu</property>
        <property name="popover">main_menu</property>
        <child>
          <object class="GtkImage">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="icon-name">open-menu-symbolic</property>
          </object>
        </child>
      </object>
      <packing>
        <property name="pack-type">end</property>
        <property name="position">1</property>
      </packing>
    </child>
    <child>
      <object class="GtkButtonBox" id="open_button_box">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <property name="layout-style">expand</property>
        <child>
          <object class="GtkButton">
            <property name="label" translatable="yes">_Open</property>
            <property name="name">open-button</property>
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="tooltip-text" translatable="yes">Open a project</property>
            <property name="use-underline">True</property>
            <property name="always-show-image">True</property>
            <signal name="clicked" handler="cb_open" swapped="no"/>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">0</property>
            <property name="non-homogeneous">True</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="position">1</property>
      </packing>
    </child>
    <child>
      <placeholder/>
    </child>
    <child>
      <object class="GtkButton">
        <property name="name">new-button</property>
        <property name="visible">True</property>
        <property name="can-focus">True</property>
        <property name="receives-default">True</property>
        <property name="tooltip-text" translatable="yes">Create a new file</property>
        <signal name="clicked" handler="cb_new" swapped="no"/>
        <child>
          <object class="GtkImage">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="icon-name">document-new-symbolic</property>
          </object>
        </child>
      </object>
      <packing>
        <property name="position">2</property>
      </packing>
    </child>
    <child>
      <object class="GtkButtonBox" id="save_button_box">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <property name="layout-style">expand</property>
        <child>
          <object class="GtkButton">
            <property name="label" translatable="yes">_Save</property>
            <property name="name">save-button</property>
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="tooltip-text" translatable="yes">Save the current project</property>
            <property name="use-underline">True</property>
            <signal name="clicked" handler="cb_save" swapped="no"/>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton">
            <property name="name">save-as-button</property>
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="tooltip-text" translatable="yes">Save the current project with a different name</property>
            <property name="use-underline">True</property>
            <signal name="clicked" handler="cb_save_as" swapped="no"/>
            <child>
              <object class="GtkImage">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <property name="icon-name">document-save-as-symbolic</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="pack-type">end</property>
        <property name="position">3</property>
      </packing>
    </child>
    <child>
      <placeholder/>
    </child>
  </object>
</interface>
"""
                
win = Main_Window()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
