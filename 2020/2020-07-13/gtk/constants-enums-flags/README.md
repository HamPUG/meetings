# Constants, Enums and Flags

The program **get_module_classes_constants.py** is a utility to extract constants, enums and flags for the Gtk module.
It returns two csv files:

* Gtk_class.csv

...is a list of all the classes for Gtk.

* Gtk_constant.csv

...is a list of all constants, enums or flags. As well as the Gtk class name it includes a type() and an eval() For examples:

```
Gtk.MAJOR_VERSION,<class 'int'>,3
Gtk.Align.CENTER,<class 'gi.repository.Gtk.Align'>,<enum GTK_ALIGN_CENTER of type Gtk.Align>
```
The program may be edited at about line 45. Instead receiving information for Gtk, you can get it for other modules.
E.g.
```
#module_list = ["Gtk"]
module_list = ["sys", "os"]
```
