#!/usr/bin/python3
import pathlib
import tkinter.ttk as ttk
import pygubu
from tkinter import filedialog as fd

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "first_ui.ui"


class FirstUiApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)
        self.mainwindow.bind("<Control-o>", self.on_file_open_click)

        self.scale_var = None
        self.check_var = None
        builder.import_variables(self, ['scale_var', 'check_var'])

        self.scale_var.set(12)
        self.check_var.set("true")

    def run(self):
        self.mainwindow.mainloop()

    def on_file_open_click(self, widget_id=None):
        filetypes = (
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title="Open text file",
            initialdir=".",
            filetypes=filetypes)
        print(filename)
        

    def on_file_close_click(self, widget_id=None):
        print("close")
        self.mainwindow.quit()

    def on_button1_click(self, widget_id=None):
        print(widget_id)
        print(self.scale_var.get())

    def on_button2_click(self):
        print(self.check_var.get())


if __name__ == "__main__":
    app = FirstUiApp()
    app.run()

