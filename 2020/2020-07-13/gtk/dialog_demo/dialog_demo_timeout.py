#!/usr/bin/env python3
#
# dialog_demo_timeout.py
#
# Example of a Gtk.MessageDialog displaying a message for a few seconds and then
# destroying itself.
#
# Utilises GLib.timeout_add_seconds() to trigger the closing of the 
# MessageDialog
#
# ian Stewart 2020-06-29
#
import sys
import datetime
import random

# Version checking - although specific versions are not required in all cases.
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, GLib #Pango #Gst, GObject, Gtk, Gdk,
# Gtk 3.24.18 	2018-09-03, Gtk 4.0 Oct/Nov? 2020
print("\nGtk Version:", Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION)


class Main_Window(Gtk.Window):
    'Launch the GTK window'
    def __init__(self):
        super(Main_Window, self).__init__()
        
        # Setup the main window       
        self.setup_window()
        
        # First time message dialog is launched by the code below.
        # Afterwards launched by the OK button callback.
        time_out = random.randint(1, 5)
        time_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        
        #fontdesc = pango.FontDescription("monospace")
        #dialog.modify_font(fontdesc) 
        #self.modify_font(Pango.FontDescription('Mono'))
        
        # Launch Gtk.MessageDialog()
        # If markup used then it support bold and italic, etc.
        
        self.message_dialog_timeout("Auto-timeout Message.", 
                "Message posted at: <b><big>{}</big></b>. \n "
                "<tt>Random timeout of <b><big>{}</big></b> seconds.</tt>"
                .format(time_string, time_out), time_out)  
        
        # Start
        Gtk.main()
        # Shutdown actions
        self.destroy()
        sys.exit()


    def message_dialog_timeout(self, title="Heading", text="End is near", timeout=2):
        """
        Use dialog to display a message and then destroy the dialog after a 
        timeout period.
        """
        # Create the dialog
        # Gtk.ButtonsType: CANCEL, CLOSE, NONE, OK, OK_CANCEL, YES_NO
        dialog = Gtk.MessageDialog(parent = self,
                                modal = True, destroy_with_parent = True,
                                message_type = Gtk.MessageType.WARNING,
                                buttons = Gtk.ButtonsType.NONE,
                                title = title)

        #dialog.format_secondary_text(text)
        #print(dialog.get_css_name())  # messagedialog


        # DeprecationWarning: Gtk.Widget.modify_font is deprecated
        #dialog.modify_font(Pango.FontDescription('Mono'))
        #dialog.modify_font(Pango.FontDescription("sans 16 italic"))
        #dialog.format_secondary_markup(text)
        dialog.format_secondary_markup(text)      
       
        # Gtk.WindowPosition: 'CENTER', 'CENTER_ALWAYS', 'CENTER_ON_PARENT', 
        # 'MOUSE', 'NONE'
        dialog.set_position(Gtk.WindowPosition.MOUSE) 

        def timeout_now():
            dialog.response(Gtk.ResponseType.OK)
 
        GLib.timeout_add_seconds(timeout, timeout_now)                

        if dialog.run() == Gtk.ResponseType.OK:        
            dialog.destroy()
            return


    def setup_window(self):
        # Setup window
        self.set_title("Dialog Demo - Timeout and Destroy")
        #self.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_default_size(500, 400)
        self.connect("destroy", Gtk.main_quit, "WM destroy")
        self.set_position(Gtk.WindowPosition.MOUSE)
        
        # Set up widgets, Vbox and Labels
        self.vbox = Gtk.VBox() 
        self.label_1 = Gtk.Label()
        self.label_1.set_text("Click button to display a message that times out:")
        self.vbox.pack_start(self.label_1, expand=False, fill=False, padding=0)
        
        self.button_1 = Gtk.Button()
        self.button_1.set_label("Click for message")
        self.button_1.connect("clicked", self.button_1_callback)
        self.vbox.pack_start(self.button_1, expand=False, fill=False, padding=0)
        self.add(self.vbox)
        self.show_all()
        
        
    def button_1_callback(self, button_widget):
            """
            Launch message dialog for a random amount of time.
            Message dialog is automatically destroyed
            """
            time_out = random.randint(1, 5)
            time_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Launch Gtk.MessageDialog()
            self.message_dialog_timeout("Auto-timeout Message.", 
                "Message posted at: <b><big>{}</big></b>. \n "
                "<tt>Random timeout of <b><big>{}</big></b> seconds.</tt>"
                .format(time_string, time_out), time_out)             
               

if __name__ == "__main__":           
    Gtk.init()
    Main_Window()
    
"""

https://developer.gnome.org/pango/unstable/pango-Markup.html
    <b>: Bold
    <big>: Makes font relatively larger, equivalent to <span size="larger">
    <i>: Italic
    <s>: Strikethrough
    <sub>: Subscript
    <sup>: Superscript 
    <small>: Makes font relatively smaller, equivalent to <span size="smaller"> 
    <tt>: Monospace  
    <u>: Underline
"""
