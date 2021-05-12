# GTK Widgets

## Featuring the Gtk.HeaderBar

Ian Stewart presented using GTK in a way in which some widgets are loaded using the manual/conventional method in combination 
with using Glade and Builder to load some other widgets.

The objective behind doing this is as follows...

In creating a GTK GUI application, some widgets and their associated code is repetitive. These widgets and their callback 
signals are designed in the Glade environment and this creates an XML User interface file. On launching the GTK application 
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
