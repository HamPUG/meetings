import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self, builder):
        super().__init__(title="Hello Glade")
        builder.connect_signals(self)
        window = builder.get_object("window_main")
        window.show_all()
        Gtk.main()

    def gtk_main_quit(self, *args):
        Gtk.main_quit(*args)


builder = Gtk.Builder()
builder.add_from_file(os.path.dirname(__file__) + "/glade_gui.glade")
MyWindow(builder)

