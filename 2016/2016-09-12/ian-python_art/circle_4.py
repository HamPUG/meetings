#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Program: circle_4
#
# A program that contains auto-generated tk() widgets
#
# MIT License (MIT)
# Copyright (c) 2016 Ian Stewart
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.
#
# Import Modules
import sys
import os
import math

if int(sys.version[0]) < 3:
    sys.exit("Python version not supported. Please use python3")

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

# Variables and Constants
debug = False
FONT = ('FreeSans', 12, "normal")

PROGRAM = 'circle_4'
TITLE = 'Circle Area Calculator'
GENERATOR_VERSION = '1.0'
CODE_VERSION = 'AA-160909-235425-060523'

MSGBOX_TITLE = 'Circle Area Calculator'
MSGBOX_TEXT = ('Written in Python using tkinter templates.\n\n'
               'Ian Stewart\nSeptember 2016')
LABEL_01_001_TEXT = 'Radius:'  # id:label-radius
ENTRY_02_002_TEXT = ''  # id:entry-radius
LABEL_01_003_TEXT = 'Area:'  # id:label-area
LABEL_02_004_TEXT = ''  # id:label-area-variable

class GUI_Application(object):
    '''Launch GUI'''

    def __init__(self, parent):
        '''Initialization of this class'''
        #ttk.Frame.__init__(self, parent)
        # print(dir(self))
        # print(dir(parent))
        self.parent = parent
        # Setup the parent window
        # Config the border just so it can be initiall seen...
        self.parent.configure(borderwidth=2) #, relief="flat", background="pink")
        # Initially force GUI geometry width x height + position x + position y
        #self.parent.geometry('300x150+100+200')
        self.parent.title(TITLE)
        self.create_frames()
        self.create_menu(parent)
        self.create_widgets()
        self.action_on_launch()

    # ===== Start of Menubar Section =====
    def create_menu(self, parent):
        # Create the default options for saving the prime numbers to a file
        # https://tkinter.unpythonic.net/wiki/tkFileDialog # Old V2.7 example
        # -confirmoverwrite, -defaultextension, -filetypes, -initialdir,
        # -initialfile, -parent, -title, or -typevariable
        
        # Create a menubar for Saving data, Exit and Help information.
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        self.helpmenu = tk.Menu(menubar, tearoff=False, font=FONT)
        self.helpmenu.add_command(label="Help", command=self.help_launch)
        self.helpmenu.add_command(label="About...", command=self.help_about)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="Exit", command=self.file_exit)
        menubar.add_cascade(label="Help", menu=self.helpmenu, font=FONT)

    # ===== Menu bar call backs =====
    def help_launch(self):
        '''Launch a the help in a child window'''
        s=("This python program will calculate the area of a circle.\n"
           "The radius accepts a positive floating value point.\n"     
           "The formula used is: area = π radius²\n" 
           "Command line options:\n" 
           "\t-d --debug\n"
           "\t-h --help\n")

        top = tk.Toplevel()
        top.wm_title("Circle Area Calculator - Help")
        text = tk.Text(top, width=50, height=7, font=('FreeSans',12,"normal"))
        text.insert(tk.END, s)
        text.pack(side="top",  padx=2, pady=2)

    def help_about(self):
        '''Menubar. Help. Use a messsage box to display the About info'''
        tkmsgbox.showinfo(MSGBOX_TITLE, MSGBOX_TEXT)

    def file_exit(self):
        '''Menubar. File exit to end the program'''
        sys.exit()

    # ==== Create the Frames ======
    def create_frames(self):
        '''Create the frames. Frame 0 is the parent window frame.'''
        # Comment-out / un-comment to change to using Labelled frames.         
        self.frame_01 = ttk.Frame(self.parent,padding=(5,5,10,10), 
                borderwidth=2)
        #self.frame_01 = ttk.LabelFrame(self.parent, padding=(5,5,10,10), 
        #        borderwidth=2, text='Frame_01')
        self.frame_02 = ttk.Frame(self.parent,padding=(5,5,10,10), 
                borderwidth=2)
        #self.frame_02 = ttk.LabelFrame(self.parent, padding=(5,5,10,10), 
        #        borderwidth=2, text='Frame_02')

    # ===== Start of Widget Creation Section =====
    def create_widgets(self):
        '''Create widgets, set style, position in grid, etc. based on design'''

        # ===== Create variables and set their initial value =====
        self.entry_02_002_strvar = tk.StringVar()  # id:entry-radius
        self.entry_02_002_strvar.set(ENTRY_02_002_TEXT)  # id:entry-radius
        self.label_02_004_strvar = tk.StringVar()  # id:label-area-variable
        self.label_02_004_strvar.set(LABEL_02_004_TEXT)  # id:label-area-variable

        # ===== Create styles for use with ttk widgets =====
        self.style = ttk.Style()
        # Change the theme from default to clam
        #print(self.style.theme_names()) # ('clam', 'alt', 'default', 'classic')
        if 'clam' in self.style.theme_names():
            self.style.theme_use('clam')
        #http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-style-layer.html

        # Change a root style to modify font of all widgets.
        self.style.configure('.', font=FONT)

        # Example. Modifying the style for all button widgets... 
        #self.style.configure('TButton', background='lightblue', relief='flat')       
        # Stub for modifying style of each widget type...
        self.style.configure('TFrame',)
        self.style.configure('TLabel',)
        self.style.configure('TEntry',)

        # ===== Instantiation of widgets =====
        self.label_01_001 = ttk.Label(  # id:label-radius
                               self.frame_01,
                               text=LABEL_01_001_TEXT,
                               style='TLabel',
                               )
        vcmd=(self.parent.register(self.entry_02_002_validate),
                               '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry_02_002 = ttk.Entry(  # id:entry-radius
                               self.frame_02,
                               validate = 'all',
                               validatecommand = vcmd,
                               invalidcommand=self.entry_02_002_invalid,
                               textvariable=self.entry_02_002_strvar,
                               justify=tk.RIGHT,
                               font=('FreeSans', 14, "normal"),
                               foreground="red",
                               width=10,
                               style='TEntry',
                               )
        self.label_01_003 = ttk.Label(  # id:label-area
                               self.frame_01,
                               text=LABEL_01_003_TEXT,
                               style='TLabel',
                               )
        self.label_02_004 = ttk.Label(  # id:label-area-variable
                               self.frame_02,
                               textvariable=self.label_02_004_strvar,
                               style='TLabel',
                               )

        # ===== Grid placement geometry =====
        # Parent grid weighting
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
        # Frame placement in parent grid
        self.frame_01.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.frame_02.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        # Widget placement in frames
        self.label_01_001.grid(row=0, column=0, padx=5, pady=5, sticky='e')  # id:label-radius
        self.entry_02_002.grid(row=0, column=0, padx=5, pady=5, sticky='e')  # id:entry-radius
        self.label_01_003.grid(row=1, column=0, padx=5, pady=5, sticky='e')  # id:label-area
        self.label_02_004.grid(row=1, column=0, padx=5, pady=5, sticky='e')  # id:label-area-variable

    # ===== Last actions to perform on launching  =====
    def action_on_launch(self):
        '''Upon setup of widgets, actions to be perform can be inserted here'''
        print("Performing actions on launch...")
        pass

    # ===== Callbacks from widgets =====
    def entry_02_002_validate(self, action, index, value_if_allowed, 
                prior_value, text, validation_type, trigger_type, widget_name):
        'Validation of floating point data entered in entry widget.'
        # id:entry-radius
        if debug:print('entry_02_002_validate - trigger type is: {} text is: {}'
                    .format(trigger_type, text))

        # Floating point can have prefixs, which on their own will cause 
        # an exception with a float() test. Therefore accept the string 
        # and return a True.
        float_type = 'positive'
        #float_type = 'negative'
        #float_type = 'normal'
        if float_type == 'normal':
            float_prefix = ['', '+', '-', '0', '+0', '-0', '0.', '+0.', '-0.']
        if float_type == 'positive':
            float_prefix =['', '+', '0', '0.', '+0', '+0.']
        if float_type == 'negative':
            float_prefix =['', '-', '-0', '-0.']
        if value_if_allowed in float_prefix:
        # Maybe perform some clean-up actions here?...
            return True
        # For negative floats, force a minus sign and continue.
        if (float_type == 'negative' and index == '0' 
            and value_if_allowed in '0123456789'):
            value_if_allowed = '-' + value_if_allowed
            self.entry_02_002_strvar.set(value_if_allowed)
            self.entry_02_002.icursor('end')
        #Provide for . to become 0. or -0., -. to become -0., +. to become +0.
        if text == '.':
            if index == '0':
                self.entry_02_002_strvar.set('0.')
                self.entry_02_002.icursor('end')
                if float_type == 'negative':
                    self.entry_02_002_strvar.set('-0.')
                    self.entry_02_002.icursor('end')
                return True
            elif index == '1':
                if prior_value == '-':
                    self.entry_02_002_strvar.set('-0.')
                if prior_value == '+':
                    self.entry_02_002_strvar.set('+0.')
                self.entry_02_002.icursor('end')
                return True
        # If prefix is 0, +0 or -0, then only . may follow.
        if debug:print('prior value:'+prior_value+'	text:'+text)
        if prior_value in [ '0', '+0', '-0']:
            if text is not '.':
                return False
        # Trigger is keyboard entry. Verify if float is entered.
        if trigger_type == 'key':
            if debug:print('Trigger type: key')
            if action=='1':
                if debug:print('Action: 1. An attempted insertion')
                if text in '0123456789.':
                    try:
                        if debug:print('value if allowed:' + value_if_allowed)
                        float(value_if_allowed)
                        # Call function - pass float. For update on key
                        self.entry_02_002_insert_remove(float(value_if_allowed))
                        return True
                    except ValueError:
                        return False
                else:
                    return False
            elif action == '0':  # An attempted deletion
                if debug:print('Action: 0. An attempted deletion')
                try:
                    float(value_if_allowed)
                    # Call function - pass float. For update on key
                    self.entry_02_002_insert_remove(float(value_if_allowed))
                    return True
                except ValueError:
                    # No longer a float so maybe clear some data?...
                    return True

            elif action == '-1':  # focus in/out, or change to textvariable
                    if debug:print('Action:-1. focus in/out,change textvariable')
                    return True
            else:
                return True
        elif trigger_type == 'focusin':
            if debug:print('Trigger type: focus in')
            # Call function and pass value of entry
            self.entry_02_002_focus_in(value_if_allowed)
            return True
        elif trigger_type == 'focusout':
            if debug:print('Trigger type: focus out')
            # Call function and pass value of entry
            self.entry_02_002_focus_in(value_if_allowed)
            return True
        else:
            if debug:print('Trigger type: Something else!')  # focus, none
            return True

    def entry_02_002_invalid(self):
        'Actions taken on invalid data entry.'
        # id:entry-radius
        if debug:print('entry_02_002_invalid - data entry was invalid')

    def entry_02_002_insert_remove(self, value):
        'Entry string has had a change in the value of the float'
        # id:entry-radius
        if debug:print('entry_02_002_insert_remove - value of float: {}'
                .format(value))
        # Add your code here...
        radius = value
        area = "{:g}".format(math.pi * radius ** 2)
        self.label_02_004_strvar.set(str(area))

    def entry_02_002_focus_in(self, value):
        'On focus in clear any prompted data in the entry widget'
        # id:entry-radius
        if debug:print('entry_02_002_focus in - value if allowed: {}'
                .format(value))
        # Clear if a non-float. E.g. Remove any prompt string.
        try:
            float(self.entry_02_002_strvar.get())
        except:
            self.entry_02_002_strvar.set('')
        # Add your code here... (No guarantee the string is a float)

    def entry_02_002_focus_out(self, value):
        'On focus out, if desired, process the entry widget'
        # id:entry-radius
        if debug:print('entry_02_002_focus out - value if allowed: {}'
                .format(value))
        # Add your code here... (No guarantee the string is a float)


def help():
    "Command line option -h or --help information."
    s=("This python program will calculate the area of a circle.\n"
       "The radius accepts a positive floating value point.\n"     
       "The formula used is: area = π radius²\n" 
       "Command line options:\n" 
       "\t-d --debug\n"
       "\t-h --help\n")
    print(s)

def main():
    "Launch program."
    #print("{} launched...".format(PROGRAM))
    print("{} launched...".format(sys.argv[0]))
    root = tk.Tk()
    # Open the GUI Application class. root becomes parent in the class. 
    main_gui = GUI_Application(root)
    root.mainloop()

if __name__ == "__main__":
    # Call main routine to launch program.
    if len(sys.argv) > 1:
        if "-h" in sys.argv[1]:
            help()
            sys.exit(1)
    if len(sys.argv) > 1:
        if "-d" in sys.argv[1]:
            debug=True
    print("Launching program. For information restart with --help option")
    main()

