# GTK Widgets

## Featuring the Gtk.HeaderBar

Ian Stewart presented using GTK in a way in which some widgets are loaded using the manual/conventional method in combination 
with using Glade and Builder to load some other widgets.

The objective behind doing this is as follows...

In creating a GTK GUI application, the creation of some widgets and their associated code is repetitive. These widgets and their callback 
signals are designed in the Glade environment and this creates an XML User Interface file. On launching the GTK application 
the Gtk.Builder module reads this XML data and generates these widgets. An example of this is a GUI's Header bar and About box widgets. 
This XML data may then be used as a template and moved to GTK applications that are developed in the future.

The manual/conventional method is then used for loading the Gtk.Window and widgets specific to the requirements of this GUI application.

There are advantages in using the manual method of adding widgets in that looping code may be used to simplify adding multiple wigets 
of the same type. For example a row of buttons.

For more details please review the "gtk builder presentation" slide show in odp or pdf formats.

Demonstration code that is highlighted in the presentations includes these python programs:

* conventional_window.py
* conventional_window_with_header_bar.py
* header_bar_glade_example.py
* conventional_window_glade_components.py
* double_precision.py 

Some of the above programs expect the icon file: Icon-Gear02-Blue.svg

A breakdown of the functionality of each file:

**conventional_window.py**

Manually launched Gtk.Window with default header bar. A label is manually placed in the main window.

**conventional_window_with_header_bar.py**

Manually launched Gtk.Window with manually added Gtk.HeaderBar. A label is manually placed in the main window.

**header_bar_glade_example.py**
Manually launched Gtk.Window, but Gtk.Builder is used to read the XML file that contains the HeaderBar. A label is manually placed in 
the main window.

**conventional_window_glade_components.py**
Manually launched Gtk.Window. Gtk.Builder reads the XML file that contains a HeaderBar with buttons that Open and Save files, etc., 
plus displays the About box. A label manually placed in the main window.

**double_precision.py**
Manually launched Gtk.Window. Gtk.Builder reads the XML file that contains a HeaderBar with buttons that Open and Save files, etc., 
plus displays the About box. A label manually placed in the main window. The main feature of the program is to model double precision 
floating point data. This requires over 150 widgets to be added to the application. These are added manually using python looping 
methods rather that with Gtk.Builder and an XML file.
