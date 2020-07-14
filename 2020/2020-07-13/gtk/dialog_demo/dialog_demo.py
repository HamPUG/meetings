#!/usr/bin/env python3
#
# dialog_demo.py
#
# Example of a Gtk.MessageDialog only having an entry widget and after entering 
# text the Enter key returns the text and the dialog window is closed.
#
# ian Stewart 2020-06-28
#
import sys

# Version checking - although specific versions are not required in all cases.
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk #Gst, GObject, Gtk, Gdk, GLib
# Gtk 3.24.18 	2018-09-03, Gtk 4.0 Oct/Nov? 2020
print("\nGtk Version:", Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION)


class Main_Window(Gtk.Window):
    'Launch the GTK window'
    def __init__(self):
        super(Main_Window, self).__init__()
        
        # Setup the main window       
        self.setup_window()
        
        # Message dialog for Name...
        response = self.input_dialog("Enter Name", "Enter your name")
        print("Response:", response)
        self.label_2.set_text(str(response))        
        
        # Message dialog for password...
        response = self.input_dialog("Enter Password", "Enter Password", 
                                       "", False)
        print("Response:", response)
        self.label_2.set_text(self.label_2.get_text() + " " + str(response)) 

        # Start
        Gtk.main()
        # Shutdown actions
        self.destroy()
        sys.exit()


    def input_dialog(self, title="Heading", text="Enter Data", 
                       default_response="", visible=True):
        """
        Open a Dialog with only an entry field.
        """
        # Define a little helper function
        def entry_callback(entry):
            # After pressing Enter on entry, then force OK response.
            dialog.response(Gtk.ResponseType.OK)
            
        # Create the dialog
        # Gtk.ButtonsType: CANCEL, CLOSE, NONE, OK, OK_CANCEL, YES_NO
        dialog = Gtk.MessageDialog(parent = self,
                                modal = True, destroy_with_parent = True,
                                message_type = Gtk.MessageType.QUESTION,
                                buttons = Gtk.ButtonsType.NONE,
                                title = title)

        dialog.format_secondary_text(text)
        # Gtk.WindowPosition: 'CENTER', 'CENTER_ALWAYS', 'CENTER_ON_PARENT', 
        # 'MOUSE', 'NONE'
        dialog.set_position(Gtk.WindowPosition.MOUSE) 

        # Create an entry widget
        entry = Gtk.Entry()
        entry.set_text(default_response)
        entry.set_visibility(visible)
        entry.set_margin_start(10)
        entry.set_margin_end(10)
        entry.set_margin_bottom(5)             
        entry.connect("activate", entry_callback)

        dialog.vbox.pack_start(entry, expand=False, fill=False, padding=0)
        entry.show()

        # Run the dialog
        if dialog.run() == Gtk.ResponseType.OK:
            text = entry.get_text()
            dialog.destroy()
            return text
        else:
            # Just in case the CANCEL button is added.
            dialog.destroy()
            return None 


    def setup_window(self):
        # Setup window
        self.set_title("Dialog Demo")
        #self.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_default_size(500, 400)
        self.connect("destroy", Gtk.main_quit, "WM destroy")
        self.set_position(Gtk.WindowPosition.MOUSE)
        
        # Set up widgets, Vbox and Labels
        self.vbox = Gtk.VBox() 
        self.label_1 = Gtk.Label()
        self.label_1.set_text("Message returned from messagebox:")
        self.vbox.pack_start(self.label_1, expand=False, fill=False, padding=0)
        
        self.label_2 = Gtk.Label()
        self.label_2.set_text("")
        self.vbox.pack_start(self.label_2, expand=False, fill=False, padding=0)
        self.add(self.vbox)
        self.show_all()
        

if __name__ == "__main__":           
    Gtk.init()
    Main_Window()
