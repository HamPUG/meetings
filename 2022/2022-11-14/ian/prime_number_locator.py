#!/usr/bin/env python3
#
# Program:      prime_number_locator.py
#
# Objective:    Digital Technologies - NCEA Level 3 - example program
#               Locates prime numbers.
#               Uses the tlinter GUI
#               Progress bar uses determinate mode while locating prime
#               numbers
#
# Written for:  Hamilton Python User Group - Presentation 11 April 2016
#               https://github.com/hampug
#               http://www.meetup.com/nzpug-hamilton/
#
# Author:       Ian Stewart
#
# Date:         2016-Apr-11
# Updated:      2022-Nov-14 - Add two method using sympy
#
# Copyright:    This work is licensed under a Creative Commons
#               Attribution-ShareAlike 4.0 International License.
#               http://creativecommons.org/licenses/by-sa/4.0/
#
# Notes:
# 1. Indentation method: 4 x space characters per indentation
#
# Python modules to be imported. Plus checking
import sys
import os
import time
import math
import sympy
# Check OS platform:
# Checked on Windows 7 / 10 with python 3.4.4 - OK. 2016-07-29
#print(sys.platform) # win32
#
#if (sys.platform) == "linux" or (sys.platform) == "linux2":
#    # Program was developed on Linux so it should work OK.
#    pass
#else:
#    print("WARNING: This program was developed and tested on Linux.\n"
#          "It may need modifications for the Operating System you are using.")

# Check Python is version 3
if int(sys.version[0]) < 3:
    print("Python Version Error: Run program using python3 to support "
          "tkinter.\nExiting...")
    sys.exit()
# Import tkinter, ttk, and other tkinter modules
try:
    import tkinter as tk
except ImportError as e:
    print("Import Error: {}".format(e))
    print("tkinter module for python3 is not available.")
    print("To install tkinter: $ sudo apt-get install python3-tk")
    sys.exit(1)
try:
    from tkinter import ttk
except ImportError as e:
    print("Import Error: {}".format(e))
    print("Import Error: tkinter.ttk module is not available.")
    print("To install tkinter: $ sudo apt-get install python3-tk")
    sys.exit(1)

try:
    import tkinter.scrolledtext as tkst
except:
    print("tkinter does not include scrolled text")
    sys.exit(1)

try:
    import tkinter.messagebox as tkmsgbox
except:
    print("tkinter does not include messagebox module")
    sys.exit(1)

try:
    import tkinter.filedialog as tkfiledialog
except:
    print("tkinter does not include filedialog")
    sys.exit(1)

# Define Variables:

# Define Constants:
PROGRAM = "prime_number_locator.py"
VERSION = "1.0"
TITLE_1 = "Prime Number Locator"
TITLE_2 = "Launching tkinter/ttk application. {} {}".format(PROGRAM, VERSION)
FONT = ('FreeSans', 12, "normal")
RANGE_TUPLE = (1, 10, 100, 500, 1000, 5000, 10000)
METHOD_TUPLE = ("Divide every number", "Skip Even numbers",
                "Modulo 6 with 1 & 5", "Minimal Recursion", "sympy.primerange",
                "sympy.primerange list")
LABEL_2_TEXT = "Start From:"
LABEL_3_TEXT = "Range:"
LABEL_4_TEXT = "Method:"
LABEL_5A_TEXT = "Prime Located:"
LABEL_5B_TEXT = "Total Primes:"
LABEL_7A_TEXT = "Elapsed:"
LABEL_7B_TEXT = "Duration:"
LABEL_9_TEXT = "Prime Numbers in the range:"
BUTTON_1_TEXT = "Locate"
BUTTON_2_TEXT = "Clear"
# Constants for Help / Infomation class
HELP_FILE_LIST = ("prime_number_locator_help.txt",
                  "prime_number_locator_flow.txt",
                  "prime_number_locator_reference.txt",
                  "prime_number_locator_specification.txt")
HELP_BUTTON_TEXT_TUPLE = ("Help", "Flow", "References", "Specification")
HELP_BUTTON_TEXT_1 = ""
HELP_BUTTON_TEXT_2 = "Close"

MSGBOX_TITLE = "Prime Number locator - About..."
MSGBOX_TEXT = ("""Prime Number Locator.
An NCEA Example program.
Hamilton Python User Group.
https://github.com/hampug
Author: Ian Stewart
Date: 2016-04-11

This work is licensed under a Creative Commons
Attribution-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-sa/4.0/
""")


class HelpFrame(tk.Toplevel):

    """Open a child Toplevel window. Read in the help files and display"""

    def __init__(self):
        """Constructor for the Toplevel window"""
        tk.Toplevel.__init__(self)
        # self.geometry("400x300")
        self.title("Prime Number Locator - Information")
        self.create_widgets()

    def create_widgets(self):
        """create widgets for the help window"""
        # Information selection button
        self.help_button_text_index = 0
        self.help_button_1 = ttk.Button(self, text=HELP_BUTTON_TEXT_1,
                                        command=self.select_help_button)
        self.help_button_1.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        # Close button
        self.help_button_2 = ttk.Button(self, text=HELP_BUTTON_TEXT_2,
                                        command=self.close_help_button)
        self.help_button_2.grid(row=1, column=1, padx=5, pady=5, sticky="e")
        # Scrolled text
        self.help_scrolledtext_1 = tkst.ScrolledText(self,
                                                     wrap=tk.WORD,
                                                     bg='beige',
                                                     font=(FONT))
        self.help_scrolledtext_1.grid(row=0, column=0, columnspan=2)

        # Display the help file if it is available.
        self.select_help_button()

    def select_help_button(self):
        """Toggle that selects help, references, and specification files"""
        # Clear the Scrolled Text
        self.help_scrolledtext_1.delete(1.0, tk.END)
        # Read the text file and place in the scrolledtext
        try:
            with open(HELP_FILE_LIST[self.help_button_text_index], "r") as f:
                for line in iter(f):
                    # Skip displaying the commented out lines
                    if line[0] == "#":
                        continue
                    else:
                        # print(line)
                        self.help_scrolledtext_1.insert(tk.INSERT, line)
        except IOError as e:
            self.help_scrolledtext_1.insert(tk.INSERT,
                                            "Prime Number Locator\n{}"
                                            .format(e))
        # Update button_1 text to display title of next information
        self.help_button_text_index += 1
        if self.help_button_text_index == len(HELP_BUTTON_TEXT_TUPLE):
            self.help_button_text_index = 0
        next_text = HELP_BUTTON_TEXT_TUPLE[self.help_button_text_index]
        self.help_button_1.config(text=next_text)

    def close_help_button(self):
        """Close the help information window"""
        self.destroy()

# Main GUI application


class GUI_Prime_Number_Locator(ttk.Frame):

    """Locate the prime numbers and display"""

    def __init__(self, parent, start, range_):
        """Initilization"""
        ttk.Frame.__init__(self, parent)
        # print(dir(self))
        # print(dir(parent))
        self.parent = parent
        self.master.title(TITLE_1)
        self.create_widgets(start, range_)
        self.action_on_launch(start, range_)

    # ===== Start for Feature Section =====
    def create_widgets(self, start, range_):

        # ===== Initialization =====
        # *** Set Int variable for Entry 1
        self.entry_1_integer = tk.IntVar()
        self.entry_1_integer.set(start)

        # Set Int variable for Combobox 1
        self.combobox_1_integer = tk.IntVar()
        # Drop down list for combobox 1

        self.combobox_1_list = RANGE_TUPLE
        # Range can be based on length of string.
        # Rough passing from sys.argv range to select of range of the combobox
        range_length = len(str(range_)) - 1
        if range_length > 5:
            range_length = 5
        self.combobox_1_integer.set(self.combobox_1_list[range_length])

        # Set Str variable for Combobox 2
        self.combobox_2_string = tk.StringVar()
        # Setup Drop down list for combobox 2
        self.combobox_2_list = METHOD_TUPLE

        # ([Divide every number", Skip Even number, etc...])
        self.combobox_2_string.set(self.combobox_2_list[0])

        self.progress_bar_int = tk.IntVar()
        self.progress_bar_int.set(0)

        # Initialize Start and stop times
        self.time_start = time.time()
        self.time_stop = time.time()

        # Create the default options for saving the prime numbers to a file
        # https://tkinter.unpythonic.net/wiki/tkFileDialog # Old V2.7 example
        # -confirmoverwrite, -defaultextension, -filetypes, -initialdir,
        # -initialfile, -parent, -title, or -typevariable
        self.file_opt = options = {}
        options['confirmoverwrite'] = True
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt'), ('all files', '.*')]
        options['initialdir'] = os.getcwd()
        options['initialfile'] = "prime_numbers"
        options['parent'] = self.parent
        options['title'] = "Save Prime Numbers"
        # options['typevariable'] = ? string???

        # ===== Create styles for use with ttk widgets =====
        self.style = ttk.Style()
        # Change a root style to modify font of all widgets.
        self.style.configure('.', font=FONT)

        # ===== Create Widgets =====
        # label_1 - Not used / Reserved
        # self.label_1 = ttk.Label(self, text="", wraplength=500)
        # Label for entry
        self.label_2 = ttk.Label(self, text=LABEL_2_TEXT)
        # Create entry for start integer value. Data is validated
        self.entry_1 = ttk.Entry(self,
                                 textvariable=self.entry_1_integer,
                                 validate='key',
                                 invalidcommand=(self.register(
                                                 self.is_invalid_entry_1),
                                                 '%W', '%P'),
                                 validatecommand=(self.register(
                                                  self.is_valid_entry_1), '%P')
                                 )
        # Combobox1 label - Range of numbers for locating primes
        self.label_3 = ttk.Label(self, text=LABEL_3_TEXT)
        # Create Combobox_1
        # As combobox is "readonly" no varification of input is required.
        self.combobox_1 = ttk.Combobox(self,
                                       textvariable=self.combobox_1_integer,
                                       height=5,
                                       width=6,
                                       state="readonly",  # readwrite
                                       values=self.combobox_1_list)

        # Combobox2 label - Methods of locating primes
        self.label_4 = ttk.Label(self, text=LABEL_4_TEXT)
        # Create Combobox_2
        # Use register to define functions to validate and process invalid
        self.combobox_2 = ttk.Combobox(
            self,
            textvariable=self.combobox_2_string,
            state="readonly",  # readwrite
            values=self.combobox_2_list)

        # Labels for each Prime number located
        self.label_5 = ttk.Label(self, text=LABEL_5A_TEXT)
        self.label_6 = ttk.Label(self, text="")
        # Labels for Duration to locate prime numbers
        self.label_7 = ttk.Label(self, text=LABEL_7A_TEXT)
        self.label_8 = ttk.Label(self, text="")
        # Labels for displaying the range
        self.label_9 = ttk.Label(self, text=LABEL_9_TEXT)
        self.label_10 = ttk.Label(self, text="")
        # Scrollect Text # http://www.tutorialspoint.com/python/tk_text.htm
        self.scrolledtext_1 = tkst.ScrolledText(self,
                                                wrap=tk.WORD,
                                                height=5,
                                                bg='lightgreen',
                                                fg="black",
                                                font=(FONT))
                                                #bg='beige',
        # Button Locate
        self.button_1 = ttk.Button(self, text=BUTTON_1_TEXT,
                                   command=self.button_1_callback)
        # Button Clear
        self.button_2 = ttk.Button(self, text=BUTTON_2_TEXT,
                                   command=self.button_2_callback)
        # Create progress bar
        self.progress_bar_1 = ttk.Progressbar(self,
                                              mode='determinate',
                                              variable=self.progress_bar_int,
                                              maximum=100)
        # Create a menubar for Saving data, Exit and Help infromation.
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        self.filemenu = tk.Menu(menubar, tearoff=False, font=FONT)
        self.filemenu.add_command(label="Save", command=self.file_save)
        self.filemenu.add_command(
            label="Save As...", command=self.file_save_as)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.file_exit)
        menubar.add_cascade(label="File", menu=self.filemenu, font=FONT)
        self.helpmenu = tk.Menu(menubar, tearoff=False, font=FONT)
        self.helpmenu.add_command(label="Help", command=self.help_launch)
        self.helpmenu.add_command(label="About...", command=self.help_about)
        menubar.add_cascade(label="Help", menu=self.helpmenu, font=FONT)

        # This will disable the item at index 0 on the File menu. i.e. "Save"
        self.filemenu.entryconfig(0, state=tk.DISABLED)
        # self.filemenu.entryconfig(0, state=tk.NORMAL)

        # ===== Add widgets using grid method to the frame =====
        # self.label_1.grid(row=1, column=0, columnspan=5) # Unused
        self.label_2.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_1.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.label_3.grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.combobox_1.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.label_4.grid(row=2, column=4, padx=5, pady=5, sticky="e")
        self.combobox_2.grid(row=2, column=5, padx=5, pady=5, sticky="w")

        self.label_5.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.label_6.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.label_7.grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.label_8.grid(row=3, column=3, padx=5, pady=5, sticky="w")

        self.label_9.grid(row=0, column=1, columnspan=2, sticky="e")
        self.label_10.grid(row=0, column=3, columnspan=2, sticky="w")

        self.button_1.grid(row=3, column=4, padx=5, pady=5)
        self.button_2.grid(row=3, column=5, padx=5, pady=5)
        self.progress_bar_1.grid(row=6, column=0, columnspan=6,
                                 padx=5, pady=5, sticky="we")
        # Don't display the progress bar at this stage
        self.progress_bar_1.grid_forget()

        self.scrolledtext_1.grid(row=1, column=0, padx=5, pady=5, columnspan=6)

    def action_on_launch(self, start, range_):
        """Actions on initial launching of the application"""
        # Not used / Reserved.
        pass

    # ===== Menu bar call backs =====
    def help_launch(self):
        """Menubar. Help. The HelpFrame class to display the help"""
        subFrame = HelpFrame()

    def help_about(self):
        """Menubar. Help. Use a messsage box to display the About info"""
        tkmsgbox.showinfo(MSGBOX_TITLE, MSGBOX_TEXT)

    def file_save(self):
        """Using the defaults blindly perform a file save"""
        # "end-1c" The -1c strips the newline at the end of the text
        text = self.scrolledtext_1.get("1.0", tk.END + "-1c")
        # print(text)
        # Build the path/filename/extension
        # print(dir(os))
        # print(os.sep)
        file_path_name_ext = ("{}{}{}{}"
                              .format(self.file_opt['initialdir'],
                                      os.sep,
                                      self.file_opt['initialfile'],
                                      self.file_opt['defaultextension']))

        # print(file_path_name_ext)
        try:
            with open(file_path_name_ext, "w") as f:
                f.write(text)
        except:
            print("Failed to save")
            return

        # Disable Save menu item after perfroming the save
        self.filemenu.entryconfig(0, state=tk.DISABLED)

        # print(dir(tkfiledialog))
        # data_file = tkfiledialog.askopenfile()
        # data_file_path_name = data_file.name
        # print(data_file_path_name)
        # print(dir(file_path_name))
        # asksaveasfile

    def file_save_as(self):
        """Open dialog to save file as. Update changes from default values"""
        # "end-1c" The -1c strips the newline at the end of the text
        text = self.scrolledtext_1.get("1.0", tk.END + "-1c")
        # asksaveasfile returns and opened file. asksaveasfilename just
        # filename
        data_file = tkfiledialog.asksaveasfile(mode='w', **self.file_opt)
        # if directory path, or filename or extenxion change then remember
        # Seperate data_file.name into path, name, and extension
        # print(data_file.name)
        try:
            file_path_name_ext = data_file.name
        except AttributeError as e:
            # 'NoneType' object has no attribute 'name'
            # print("Cancelled: {}".format(e))
            return

        # Returned the files /path/name.ext which may now be different from
        # the self.file_opt values for initialdir, initialfile,
        # defaultextension
        # print(file_path_name_ext)
        path, tail = os.path.split(file_path_name_ext)
        # print(path, tail)
        filename, ext = os.path.splitext(tail)
        # print(path, filename, ext)
        # Update the default values for dir, file and extension
        self.file_opt.update(initialdir=path)
        self.file_opt.update(initialfile=filename)
        self.file_opt.update(defaultextension=ext)

        # self.file_opt(defaultextension = ext)
        # print(dir(self.file_opt))
        # print(self.file_opt.keys())
        # print(self.file_opt.values())
        # print(self.file_opt['defaultextension'])

        # TODO: If defaultextension changes then update the filetypes
        # options['filetypes'] = [('text files', '.txt'), ('all files', '.*')]
        # print(dir(data_file))

        data_file.write(text)
        data_file.close()
        # Enable the Save menu
        self.filemenu.entryconfig(0, state=tk.DISABLED)

    def file_exit(self):
        """Menubar. File exit to end the program"""
        sys.exit()

    # ===== Widget call backs =====
    def is_valid_entry_1(self, txt):
        """Check that text is only numeric in entry_1"""
        if txt.isdigit():
            return True
        else:
            return False

    def is_invalid_entry_1(self, widget_name, txt):
        """Called whenever is_valid_entry_1() returns false"""
        # non-lowercase letters have been prevented from being added to entry_1
        # Make the bell warning sound
        # >>> [m for m in dir(str) if m.startswith('is')]
        # ['isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle',
        #  'isupper']
        widget = self.nametowidget(widget_name)
        widget.bell()
        widget.focus_set()

    def button_1_callback(self):
        """Start the prime number search with progress bar"""
        # Get the currently selected method to determine which method to call
        method_index = self.combobox_2.current()

        # Two methods to obtain values of the entry and comboboxes. E.g.:
        # print(self.entry_1.get())  # Get directly
        # print(self.entry_1_integer.get())  # Get from variable
        # print(self.combobox_1.get())
        # print(self.combobox_1_integer.get())

        # Set starting point of progress bar. From 0 to maximum E.g. 100
        self.progress_bar_int.set(0)
        # Display the progress bar
        self.progress_bar_1.grid(row=6, column=0, columnspan=7,
                                 padx=5, pady=5, sticky="we")
        # Set the label to display each prime number found
        self.label_5.config(text=LABEL_5A_TEXT)
        self.label_6.config(text="")

        self.label_7.config(text=LABEL_7A_TEXT)

        # Clear the duration
        self.label_8.config(text="")
        # Get the start time
        self.time_start = time.time()

        # Get the last integer of the range
        end_integer = (self.entry_1_integer.get() +
                       self.combobox_1_integer.get())
        # Display the range
        self.label_10.config(text="{} to {}"
                             .format(self.entry_1_integer.get(),
                                     end_integer - 1))

        # ==== Select the method and call function to locate prime numbers ====
        if method_index == 0:
            # Call the prime number method and pass start and end
            primes = self.prime_number_method_0(self.entry_1_integer.get(),
                                                end_integer)
        if method_index == 1:
            # Call the prime number method and pass start and end
            primes = self.prime_number_method_1(self.entry_1_integer.get(),
                                                end_integer)

        if method_index == 2:
            # Call the prime number method and pass start and end
            primes = self.prime_number_method_2(self.entry_1_integer.get(),
                                                end_integer)
        if method_index == 3:
            # Call the prime number method and pass start and end
            primes = self.prime_number_method_3(self.entry_1_integer.get(),
                                                end_integer)

        if method_index == 4:
            # Call the prime number method and pass start and end
            primes = self.prime_number_method_4(self.entry_1_integer.get(),
                                                end_integer)

        if method_index == 5:
            # Call the prime number method and pass start and end
            primes = self.prime_number_method_5(self.entry_1_integer.get(),
                                                end_integer)

        # ===== On completing locating primes =====
        # Register the time completed
        self.time_stop = time.time()
        # Display the duration.
        self.label_7.config(text=LABEL_7B_TEXT)
        self.label_8.config(text="{0:.3f} secs"
                            .format(self.time_stop - self.time_start))

        # Change the label to give total of prime numbers found
        self.label_5.config(text=LABEL_5B_TEXT)
        self.label_6.config(text="{}".format(len(primes)))

        # Hide the progress bar
        self.progress_bar_1.grid_forget()
        # As the data has changed enable the ability to do a save
        self.filemenu.entryconfig(0, state=tk.NORMAL)

    def button_2_callback(self):
        """Clear the Scrolled Text"""
        self.scrolledtext_1.delete(1.0, tk.END)

    def prime_number_method_0(self, start_integer, end_integer):
        """
        Locate prime numbers using method 0.
        Designed to be CPU intensive. Iterates through every number.
        """
        # Locate prime numbers and place them in a list
        prime_number_list = []
        for i in range(start_integer, end_integer):
            # ==== GUI updating =====
            # Increment the progress on the Progress bar. Default is 1
            self.progress_bar_1.step(100 / (end_integer - start_integer))
            # Duration. Progress in seconds
            self.label_8.config(text="{0:.0f} secs"
                                .format(time.time() - self.time_start))
            # Refresh the GUI
            self.update_idletasks()
            # ==== End of GUI Updating =====

            # ==== Method of locating prime numbers =====
            # METHOD: Divide every number. Excessively recursive.
            count = 0
            for j in range(1, i):
                # print("i {} mod j {} = {}".format(i, j, i % j))
                if i % j == 0:
                    count += 1
            if count == 1:
                # A count of only 1 indicates a prime number
                # Place the located prime into the list
                prime_number_list.append(i)
                # ===== GUI Updating as each prime number is located =====
                # Display the located prime number
                self.label_6.config(text=str(i))
                # Insert latest found prime number in the Scrolled Text box
                self.scrolledtext_1.insert(tk.END, "{}, "
                                           .format(prime_number_list[-1]))
                # ===== End of GUI updating =====

        # print(prime_number_list)
        # print(len(prime_number_list))
        return prime_number_list

    def prime_number_method_1(self, start_integer, end_integer):
        """
        Locate prime numbers using method 1.
        Designed to be CPU intensive. Skips the even numbers.
        """
        # Locate prime numbers and place them in a list
        prime_number_list = []

        # If required, cheat and manually add the 2.
        if start_integer <= 2:
            prime_number_list.append(2)
            # Insert the prime number 2 in the Scrolled Text box
            self.scrolledtext_1.insert(tk.END, "{}, "
                                       .format(prime_number_list[-1]))

        for i in range(start_integer, end_integer):
            # ==== GUI updating =====
            # Increment the progress on the Progress bar. Default is 1
            self.progress_bar_1.step(100 / (end_integer - start_integer))
            # Duration. Progress in seconds
            self.label_8.config(text="{0:.0f} secs"
                                .format(time.time() - self.time_start))
            # Refresh the GUI
            self.update_idletasks()
            # ==== End of GUI Updating =====

            # ==== Method of locating prime numbers =====
            # METHOD: Skip the even numbers. Still excessively recursive.
            # Skip all even numbers
            if i % 2 == 0:
                continue

            count = 0
            for j in range(1, i):
                if i % j == 0:
                    count += 1

            if count == 1:
                prime_number_list.append(i)

                # ===== GUI Updating as each prime number is located =====
                # Display the located prime number
                self.label_6.config(text=str(i))
                # Insert latest found prime number in the Scrolled Text box
                self.scrolledtext_1.insert(tk.END, "{}, "
                                           .format(prime_number_list[-1]))
                # ===== End of GUI updating =====
        return prime_number_list

    def prime_number_method_2(self, start_integer, end_integer):
        """
        Locate prime numbers using method 2. Module6 remainders 1 and 5
        """
        # Locate prime numbers and place them in a list
        prime_number_list = []

        # Cheat, If required, and manually add the 2 & 3.
        if start_integer < 3:
            prime_number_list.append(2)
            # Insert the prime number 2 in the Scrolled Text box
            self.scrolledtext_1.insert(tk.END, "{}, "
                                       .format(prime_number_list[-1]))
            prime_number_list.append(3)
            # Insert the prime number 2 in the Scrolled Text box
            self.scrolledtext_1.insert(tk.END, "{}, "
                                       .format(prime_number_list[-1]))
        if start_integer == 3:
            prime_number_list.append(3)
            # Insert the prime number 3 in the Scrolled Text box
            self.scrolledtext_1.insert(tk.END, "{}, "
                                       .format(prime_number_list[-1]))

        for i in range(start_integer, end_integer):
            # ==== GUI updating =====
            # Increment the progress on the Progress bar. Default is 1
            self.progress_bar_1.step(100 / (end_integer - start_integer))
            # Duration. Progress in seconds
            self.label_8.config(text="{0:.0f} secs"
                                .format(time.time() - self.time_start))
            # Refresh the GUI
            self.update_idletasks()
            # ==== End of GUI Updating =====

            # ==== Method of locating prime numbers =====
            # METHOD: Skip all modulo 6 that do not have a remainder of 1 or 5
            if i % 6 in [0, 2, 3, 4]:
                continue
            count = 0

            for j in range(1, i):
                if i % j == 0:
                    count += 1

            if count == 1:
                prime_number_list.append(i)

                # ===== GUI Updating as each prime number is located =====
                # Display the located prime number
                self.label_6.config(text=str(i))
                # Insert latest found prime number in the Scrolled Text box
                self.scrolledtext_1.insert(tk.END, "{}, "
                                           .format(prime_number_list[-1]))
                # ===== End of GUI updating =====
        return prime_number_list

    def prime_number_method_3(self, start_integer, end_integer):
        """
        Locate prime numbers using method 3. Minimal Recursion.
        """
        # Locate prime numbers and place them in a list
        prime_number_list = []
        if start_integer < 2:
            start_integer = 2
        for i in range(start_integer, end_integer):
            # ==== GUI updating =====
            # Increment the progress on the Progress bar. Default is 1
            self.progress_bar_1.step(100 / (end_integer - start_integer))
            # Duration. Progress in seconds
            self.label_8.config(text="{0:.0f} secs"
                                .format(time.time() - self.time_start))
            # Refresh the GUI
            self.update_idletasks()
            # ==== End of GUI Updating =====

            # ==== Method of locating prime numbers =====
            # METHOD: Minimal Recursion
            for j in range(2, int(math.sqrt(i) + 1)):
                if i % j == 0:
                    break

            else:
                prime_number_list.append(i)

                # ===== GUI Updating as each prime number is located =====
                # Display the located prime number
                self.label_6.config(text=str(i))
                # Insert latest found prime number in the Scrolled Text box
                self.scrolledtext_1.insert(tk.END, "{}, "
                                           .format(prime_number_list[-1]))
                # ===== End of GUI updating =====
        return prime_number_list


    def prime_number_method_4(self, start_integer, end_integer):
        """
        Locate prime numbers using method 4. 
        Note that sympy.primerange returns a list, but this function sets a
        one integer range. so not as fast as asking for a list.
        
        https://www.sympy.org
        list(sympy.primerange(start_integer, end_integer)
        import sympy  # Computer algebra system (CAS) in Python
        SymPy is a Python library for symbolic mathematics.
        'isprime' 'prevprime', nextprime 'prime', 'primefactors', 'primenu', 
        'primeomega', 'primepi', 'primerange',
        
        airyaiprime, airybiprime, is_mersenne_prime, mathieucprime, mathieusprime
        mersenne_prime_exponent randprime, ratsimpmodprime
        """
        # Locate prime numbers and place them in a list
        prime_number_list = []
        if start_integer < 2:
            start_integer = 2
        for i in range(start_integer, end_integer):
            # ==== GUI updating =====
            # Increment the progress on the Progress bar. Default is 1
            self.progress_bar_1.step(100 / (end_integer - start_integer))
            # Duration. Progress in seconds
            self.label_8.config(text="{0:.0f} secs"
                                .format(time.time() - self.time_start))
            # Refresh the GUI
            self.update_idletasks()
            # ==== End of GUI Updating =====

            # ==== Method of locating prime numbers =====
            # METHOD: Using sympy.primerange
            #for j in range(2, int(math.sqrt(i) + 1)):
            #    if i % j == 0:
            #        break

            temp_list = list(sympy.primerange(i, i+1))
            if len(temp_list) == 0:
                continue
                
            else:
                prime_number_list.append(temp_list[0])

                # ===== GUI Updating as each prime number is located =====
                # Display the located prime number
                self.label_6.config(text=str(i))
                # Insert latest found prime number in the Scrolled Text box
                self.scrolledtext_1.insert(tk.END, "{}, "
                                           .format(prime_number_list[-1]))
                # ===== End of GUI updating =====
        return prime_number_list


    def prime_number_method_5(self, start_integer, end_integer):
        """
        Locate prime numbers using method 4. 
        Note that sympy.primerange returns a list, but this function sets a
        one integer range. so not as fast as asking for a list.
        
        https://www.sympy.org
        list(sympy.primerange(start_integer, end_integer)
        import sympy  # Computer algebra system (CAS) in Python
        SymPy is a Python library for symbolic mathematics.
        'isprime' 'prevprime', nextprime 'prime', 'primefactors', 'primenu', 
        'primeomega', 'primepi', 'primerange',
        
        airyaiprime, airybiprime, is_mersenne_prime, mathieucprime, mathieusprime
        mersenne_prime_exponent randprime, ratsimpmodprime
        """
        #print( start_integer, end_integer)
        # Locate prime numbers and place them in a list
        #prime_number_list = []
        if start_integer < 2:
            start_integer = 2
            
        prime_number_list = list(sympy.primerange(start_integer, end_integer))            
        
        #print(type(prime_number_list))  # list
        #print(len(prime_number_list))  # 6
        #self.label_6.config(text=str(i))
        # Insert latest found prime number in the Scrolled Text box
        
        for prime_number in prime_number_list:
            self.scrolledtext_1.insert(tk.END, "{}, "
                                           .format(prime_number))

            
        return prime_number_list            
            
        """    
        for i in range(start_integer, end_integer):
            # ==== GUI updating =====
            # Increment the progress on the Progress bar. Default is 1
            self.progress_bar_1.step(100 / (end_integer - start_integer))
            # Duration. Progress in seconds
            self.label_8.config(text="{0:.0f} secs"
                                .format(time.time() - self.time_start))
            # Refresh the GUI
            self.update_idletasks()
            # ==== End of GUI Updating =====

            # ==== Method of locating prime numbers =====
            # METHOD: Using sympy.primerange
            #for j in range(2, int(math.sqrt(i) + 1)):
            #    if i % j == 0:
            #        break


            if len(temp_list) == 0:
                continue
                
            else:
                prime_number_list.append(temp_list[0])

                # ===== GUI Updating as each prime number is located =====
                # Display the located prime number
                self.label_6.config(text=str(i))
                # Insert latest found prime number in the Scrolled Text box
                self.scrolledtext_1.insert(tk.END, "{}, "
                                           .format(prime_number_list[-1]))
                # ===== End of GUI updating =====
        return prime_number_list
        """


if __name__ == "__main__":
    """Check for command line arguments."""
    print(TITLE_2)

    # Check for start integer
    if len(sys.argv) > 1:
        if sys.argv[1].isdigit():
            start = int(sys.argv[1])
        else:
            print("Prime number locator options: [start integer] and [range]")
            sys.exit(1)
    else:
        start = 100000  # Default value of 100000 to take time

    # Check for range
    if len(sys.argv) > 2:
        if sys.argv[2].isdigit():
            range_ = int(sys.argv[2])
        else:
            range_ = 100
    else:
        range_ = 100

    # Launch tkinter GUI.
    root = tk.Tk()

    # Force the geometry of the GUI width x height + position x + position y
    # root.geometry('1000x180+100+100')
    # Open the GUI Application class. Use grid to place in different rows
    # Add the sticky="we" - Expands the grey background area
    main_gui = (GUI_Prime_Number_Locator(root, start, range_)
                .grid(row=0, column=0, sticky="we"))

    root.mainloop()

'''
Notes:
Progress Bar:
You must be using: self.pgBar.step(x) where 'x' is the amount to be increased
in progressbar. For this to get updated in your UI you have to put
self.update_idletasks() after every self.pgBar.step(x) statement.

         1         2         3         4         5         6         7        7
1234567890123456789012345678901234567890123456789012345678901234567890123456789
'''
