#!/usr/bin/env python3
#!
# python-help-gui-gtk4.py
#
# The python help categories; topics, symbols, modules, and keywords
# are made selectable with a mouse click. The help information is then 
# displayed in a scrollable window. 
#
# Tested on: 
# manjaro 21.2.2 / python 3.10.5
# 
# Ian Stewart - CC0
#  
import sys
import os
import contextlib
from io import StringIO
import gi
try: 
    gi.require_version("Gtk", "4.0")
except ValueError as e:
    print(e)
    sys.exit("Unable to run {} program. Exiting...".format(sys.argv[0]))
from gi.repository import Gtk, Gdk, Gio

# version
VERSION = "2022-08-03"
# Gtk version
GTK_VERSION = "{}.{}.{}".format(Gtk.get_major_version(), Gtk.get_minor_version(),
        Gtk.get_micro_version())
# Clicks to select items. Default is double-click ==> SINGLE_CLICK = False
SINGLE_CLICK = True
# Provide the column header with a heading.
COLUMN_HEADING = 'Help Categories'
# Welcome message
WELCOME = """
Welcome to Python Help Gui 
Version:{}. 
Gtk Version:{}. 
App:{}

Select a Help Category and then an item within the category.
""".format(VERSION, GTK_VERSION, sys.argv[0])


class Window(Gtk.Window):
    def __init__(self, **kwargs):    
        super(Window, self).__init__(**kwargs)
        
        # Add the title to the window
        version = sys.version.split(" ")[0]
        self.set_title("Help for Python version {}".format(version))      
        # Set default window size
        self.set_default_size(1400, 600)
        
        self.grid = Gtk.Grid()
        self.set_child(self.grid)

        self.create_textview()
        self.setup_treeview()
        self.set_style()  
        self.textbuffer.set_text(WELCOME)

    def set_style(self):
        """ Loads custom CSS for textview and treeview"""
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(b"""
        #textview { 
            font: 16px "Monospace";
            margin: 10px;
            /*color: #000000;  Black conflicts with dark theme*/ 
            }
        #treeview {
            font: 14px Sans;
            margin: 10px;
            /* border-width: 10px; Around the column header */
            }
        """)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), 
                style_provider, 
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
                
    def create_textview(self):
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)        

        self.grid.attach(scrolled_window, 0, 0, 5, 1)        

        self.textview = Gtk.TextView()
        self.textview.set_name("textview")        
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("")
        scrolled_window.set_child(self.textview)

    def setup_treeview(self):
        # Create a window that can be scrolled
        scrolled_window = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        #scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)  
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        # Create a TreeStore with one string column to use as the model
        store = Gtk.TreeStore(str)
        # From help dictionary add the categories and items to the store 
        for category, items in help_dict.items():
            category_key = store.append(None, [category])
            for item in items:
                store.append(category_key,[item])
                        
        # Create the TreeView using Treestore
        self.treeview = Gtk.TreeView()
        self.treeview.set_model(store)

        # Set unique name so css can be applied to widget
        self.treeview.set_name("treeview")

        # Preference for self.treeview. Adjust via contants at start of progrma
        self.treeview.set_activate_on_single_click(SINGLE_CLICK)
        
        treeview_column = Gtk.TreeViewColumn(COLUMN_HEADING)
        self.treeview.append_column(treeview_column)

        cell = Gtk.CellRendererText()

        treeview_column.pack_start(cell, True)
        treeview_column.add_attribute(cell, 'text', 0)

        # connect the self.treeview
        self.treeview.connect ("row-activated", self.cb_on_row_activate,)

        #scrolled_window.add(self.treeview)
        scrolled_window.set_child(self.treeview)
        self.grid.attach(scrolled_window, 6, 0, 1, 1) 

    def cb_on_row_activate (self, treeview, path, column,):
        ' Call back when click on a row in the treeview. Select station'
        model = treeview.get_model()
        iter  = model.get_iter (path)

        # Don't want the categories only the items which have two fields
        pointer_list = path.to_string().split(":")
        if len(pointer_list) == 2:
            self.item_selected = model[iter][0]
            # Update the title to reflect selected item
            version = sys.version.split(" ")[0]
            self.set_title("Help for Python version {} - Selection: {}"
                    .format(version, self.item_selected)) 
            # Retrieve the help information and display 
            info = get_help(self.item_selected)
            self.textbuffer.set_text(info)


class Application(Gtk.Application):
    ''' Main Application class '''
    def __init__(self):
        super().__init__(application_id='gtk4.python.help',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = Window(application=self)
        win.present()
                

# Initial setup / data collection routines, etc.
def get_help(func):
    """
    Write the output of help() to a text buffer and return as text string.
    Usage example: get_help("float")
    Requires: contextlib and io.StringIO
    """
    output = StringIO()
    with contextlib.redirect_stdout(output):
        help(func)       
    contents = output.getvalue()
    output.close()
    return contents


def get_help_list(data):
    """
    Python help has categories of topics, symbols and keywords.
    These topics are displayed in four columns
    Convert the category into a list and sort alphabetically
    """
    new_data = data.replace("\n", " ")  # change newlines to spaces.
    position = new_data.find("help.")  # Find end of heading
    new_data = new_data[position+5:]  # Start after heading
    data_list = new_data.split(" ")
         
    # Clear the list of empty fields using pop()
    data_len_index = len(data_list) - 1
    for index, item in enumerate(reversed(data_list)):
        if item == "":
            data_list.pop(data_len_index - index)
                        
    data_list.sort()
    return data_list
 

def get_help_module_list(data):
    """
    Python help has a list of modules.
    These topics normally are displayed in four columns
    The get_help() has produced a variable containing string data.
    Convert the data to a list and sort alphabetically
    """
    # Remove trailing message text in the data
    position = data.find("Enter any module name to get more help.")
    data = data[:position]
    
    # Remove leading message "a list of all available modules..." 35 chars
    position = data.find("a list of all available modules...")
    data = data[position+35:]
    
    # Split data into lines for removal of INFO and DEBUG
    data_line_list = data.split("\n")
    new_data_line_list = []
    for line in data_line_list:
        if (line.startswith("INFO:") or line.startswith("DEBUG:") or 
                line.startswith("WARNING:")):
            continue
        else:
            new_data_line_list.append(line)
            
    # Rebuild as string but with newlines replaced by spaces
    data = " ".join(new_data_line_list)
    # Split into a list based on spaces.
    data_list = data.split(" ")
    
    # Clear the list of empty fields using reverse pop()
    data_len_index = len(data_list) - 1
    for index, item in enumerate(reversed(data_list)):
        if item == "":
            data_list.pop(data_len_index - index)
            
    data_list.sort()
    return data_list
 
        
if __name__=="__main__":

    print("""
    Collecting information and setting up Python Help Gui application.
    
    This will take a few moments and then the GUI will launch.
    
    Any messages displayed below are likely to be related to >>> help('modules')
    
    """)
    
    # Get the data and build the dictionary to pass data to TreeStore/TreeView
    help_dict = {}
    
    keywords = get_help("keywords")
    keyword_data_list = get_help_list(keywords)
    help_dict["Keywords"] = keyword_data_list
    
    symbols = get_help("symbols")
    symbol_data_list = get_help_list(symbols)
    help_dict["Symbols"] = symbol_data_list
        
    topics = get_help("topics")
    topic_data_list = get_help_list(topics)
    help_dict["Topics"] = topic_data_list

    # Note: help(modules) takes quite a bit of time to perform. e.g. 30 seconds.
    modules = get_help("modules")  
    module_data_list = get_help_module_list(modules)           
    help_dict["Modules"] = module_data_list
    
    # Run the application
    app = Application()
    app.run(sys.argv)    
"""
Reference:
https://athenajc.gitbooks.io/python-gtk-3-api/content/gtk-group/gtktreestore.html
"""
