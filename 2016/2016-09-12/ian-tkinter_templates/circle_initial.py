#!/usr/bin/env python3
#
# Program: circle
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

# Check python3
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

PROGRAM = 'circle'
TITLE = 'circle'
GENERATOR_VERSION = '1.0'
CODE_VERSION = 'AA-160915-025606-587671'

LABEL_01_001_TEXT = 'label_01_001'  # id:radius-label
ENTRY_01_002_TEXT = 'entry_01_002_validate'  # id:radius-entry
LABEL_02_003_TEXT = 'label_02_003'  # id:diameter-text
LABEL_02_004_TEXT = 'label_02_004-strvar'  # id:diameter-variable
LABEL_02_005_TEXT = 'label_02_005'  # id:circumference-text
LABEL_02_006_TEXT = 'label_02_006-strvar'  # id:circumference-variable
LABEL_02_007_TEXT = 'label_02_007'  # id:area-text
LABEL_02_008_TEXT = 'label_02_008-strvar'  # id:area-variable
LABEL_03_009_TEXT = 'label_03_009'  # id:surface-text
LABEL_03_010_TEXT = 'label_03_010-strvar'  # id:surface-variable
LABEL_03_011_TEXT = 'label_03_011'  # id:volume-text
LABEL_03_012_TEXT = 'label_03_012-strvar'  # id:volume-variable

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
        self.parent.configure(borderwidth=2, relief="flat", background="pink")
        # Initially force GUI geometry width x height + position x + position y
        #self.parent.geometry('300x150+100+200')
        self.parent.title(TITLE)
        self.create_frames()
        self.create_widgets()
        self.action_on_launch()

    # ==== Create the Frames ======
    def create_frames(self):
        '''Create the frames. Frame 0 is the parent window frame.'''
        # Comment-out / un-comment to change to using Labelled frames.         
        #self.frame_01 = ttk.Frame(self.parent,padding=(5,5,10,10), 
        #        borderwidth=2)
        self.frame_01 = ttk.LabelFrame(self.parent, padding=(5,5,10,10), 
                borderwidth=2, text='Frame_01')
        #self.frame_02 = ttk.Frame(self.parent,padding=(5,5,10,10), 
        #        borderwidth=2)
        self.frame_02 = ttk.LabelFrame(self.parent, padding=(5,5,10,10), 
                borderwidth=2, text='Frame_02')
        #self.frame_03 = ttk.Frame(self.parent,padding=(5,5,10,10), 
        #        borderwidth=2)
        self.frame_03 = ttk.LabelFrame(self.parent, padding=(5,5,10,10), 
                borderwidth=2, text='Frame_03')

    # ===== Start of Widget Creation Section =====
    def create_widgets(self):
        '''Create widgets, set style, position in grid, etc. based on design'''

        # ===== Create variables and set their initial value =====
        self.entry_01_002_strvar = tk.StringVar()  # id:radius-entry
        self.entry_01_002_strvar.set(ENTRY_01_002_TEXT)  # id:radius-entry
        self.label_02_004_strvar = tk.StringVar()  # id:diameter-variable
        self.label_02_004_strvar.set(LABEL_02_004_TEXT)  # id:diameter-variable
        self.label_02_006_strvar = tk.StringVar()  # id:circumference-variable
        self.label_02_006_strvar.set(LABEL_02_006_TEXT)  # id:circumference-variable
        self.label_02_008_strvar = tk.StringVar()  # id:area-variable
        self.label_02_008_strvar.set(LABEL_02_008_TEXT)  # id:area-variable
        self.label_03_010_strvar = tk.StringVar()  # id:surface-variable
        self.label_03_010_strvar.set(LABEL_03_010_TEXT)  # id:surface-variable
        self.label_03_012_strvar = tk.StringVar()  # id:volume-variable
        self.label_03_012_strvar.set(LABEL_03_012_TEXT)  # id:volume-variable

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
        self.label_01_001 = ttk.Label(  # id:radius-label
                               self.frame_01,
                               text=LABEL_01_001_TEXT,
                               style='TLabel',
                               )
        vcmd=(self.parent.register(self.entry_01_002_validate),
                               '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry_01_002 = ttk.Entry(  # id:radius-entry
                               self.frame_01,
                               validate = 'all',
                               validatecommand = vcmd,
                               invalidcommand=self.entry_01_002_invalid,
                               textvariable=self.entry_01_002_strvar,
                               style='TEntry',
                               )
        self.label_02_003 = ttk.Label(  # id:diameter-text
                               self.frame_02,
                               text=LABEL_02_003_TEXT,
                               style='TLabel',
                               )
        self.label_02_004 = ttk.Label(  # id:diameter-variable
                               self.frame_02,
                               textvariable=self.label_02_004_strvar,
                               style='TLabel',
                               )
        self.label_02_005 = ttk.Label(  # id:circumference-text
                               self.frame_02,
                               text=LABEL_02_005_TEXT,
                               style='TLabel',
                               )
        self.label_02_006 = ttk.Label(  # id:circumference-variable
                               self.frame_02,
                               textvariable=self.label_02_006_strvar,
                               style='TLabel',
                               )
        self.label_02_007 = ttk.Label(  # id:area-text
                               self.frame_02,
                               text=LABEL_02_007_TEXT,
                               style='TLabel',
                               )
        self.label_02_008 = ttk.Label(  # id:area-variable
                               self.frame_02,
                               textvariable=self.label_02_008_strvar,
                               style='TLabel',
                               )
        self.label_03_009 = ttk.Label(  # id:surface-text
                               self.frame_03,
                               text=LABEL_03_009_TEXT,
                               style='TLabel',
                               )
        self.label_03_010 = ttk.Label(  # id:surface-variable
                               self.frame_03,
                               textvariable=self.label_03_010_strvar,
                               style='TLabel',
                               )
        self.label_03_011 = ttk.Label(  # id:volume-text
                               self.frame_03,
                               text=LABEL_03_011_TEXT,
                               style='TLabel',
                               )
        self.label_03_012 = ttk.Label(  # id:volume-variable
                               self.frame_03,
                               textvariable=self.label_03_012_strvar,
                               style='TLabel',
                               )

        # ===== Grid placement geometry =====
        # Parent grid weighting
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
        self.parent.columnconfigure(2, weight=1)
        # Frame placement in parent grid
        self.frame_01.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.frame_02.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.frame_03.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        # Widget placement in frames
        self.label_01_001.grid(row=0, column=0, padx=5, pady=5, sticky='w')  # id:radius-label
        self.entry_01_002.grid(row=1, column=0, padx=5, pady=5, sticky='w')  # id:radius-entry
        self.label_02_003.grid(row=0, column=0, padx=5, pady=5, sticky='w')  # id:diameter-text
        self.label_02_004.grid(row=1, column=0, padx=5, pady=5, sticky='w')  # id:diameter-variable
        self.label_02_005.grid(row=2, column=0, padx=5, pady=5, sticky='w')  # id:circumference-text
        self.label_02_006.grid(row=3, column=0, padx=5, pady=5, sticky='w')  # id:circumference-variable
        self.label_02_007.grid(row=4, column=0, padx=5, pady=5, sticky='w')  # id:area-text
        self.label_02_008.grid(row=5, column=0, padx=5, pady=5, sticky='w')  # id:area-variable
        self.label_03_009.grid(row=0, column=0, padx=5, pady=5, sticky='w')  # id:surface-text
        self.label_03_010.grid(row=1, column=0, padx=5, pady=5, sticky='w')  # id:surface-variable
        self.label_03_011.grid(row=2, column=0, padx=5, pady=5, sticky='w')  # id:volume-text
        self.label_03_012.grid(row=3, column=0, padx=5, pady=5, sticky='w')  # id:volume-variable

    # ===== Last actions to perform on launching  =====
    def action_on_launch(self):
        '''Upon setup of widgets, actions to be perform can be inserted here'''
        print("Performing actions on launch...")
        pass

    # ===== Callbacks from widgets =====
    def entry_01_002_validate(self, action, index, value_if_allowed, 
                prior_value, text, validation_type, trigger_type, widget_name):
        'Validation of floating point data entered in entry widget.'
        # id:radius-entry
        if debug:print('entry_01_002_validate - trigger type is: {} text is: {}'
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
            self.entry_01_002_strvar.set(value_if_allowed)
            self.entry_01_002.icursor('end')
        #Provide for . to become 0. or -0., -. to become -0., +. to become +0.
        if text == '.':
            if index == '0':
                self.entry_01_002_strvar.set('0.')
                self.entry_01_002.icursor('end')
                if float_type == 'negative':
                    self.entry_01_002_strvar.set('-0.')
                    self.entry_01_002.icursor('end')
                return True
            elif index == '1':
                if prior_value == '-':
                    self.entry_01_002_strvar.set('-0.')
                if prior_value == '+':
                    self.entry_01_002_strvar.set('+0.')
                self.entry_01_002.icursor('end')
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
                        self.entry_01_002_insert_remove(float(value_if_allowed))
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
                    self.entry_01_002_insert_remove(float(value_if_allowed))
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
            self.entry_01_002_focus_in(value_if_allowed)
            return True
        elif trigger_type == 'focusout':
            if debug:print('Trigger type: focus out')
            # Call function and pass value of entry
            self.entry_01_002_focus_in(value_if_allowed)
            return True
        else:
            if debug:print('Trigger type: Something else!')  # focus, none
            return True

    def entry_01_002_invalid(self):
        'Actions taken on invalid data entry.'
        # id:radius-entry
        if debug:print('entry_01_002_invalid - data entry was invalid')

    def entry_01_002_insert_remove(self, value):
        'Entry string has had a change in the value of the float'
        # id:radius-entry
        if debug:print('entry_01_002_insert_remove - value of float: {}'
                .format(value))
        # Add your code here...

    def entry_01_002_focus_in(self, value):
        'On focus in clear any prompted data in the entry widget'
        # id:radius-entry
        if debug:print('entry_01_002_focus in - value if allowed: {}'
                .format(value))
        # Clear if a non-float. E.g. Remove any prompt string.
        try:
            float(self.entry_01_002_strvar.get())
        except:
            self.entry_01_002_strvar.set('')
        # Add your code here... (No guarantee the string is a float)

    def entry_01_002_focus_out(self, value):
        'On focus out, if desired, process the entry widget'
        # id:radius-entry
        if debug:print('entry_01_002_focus out - value if allowed: {}'
                .format(value))
        # Add your code here... (No guarantee the string is a float)


def help():
    "Command line option -h or --help information."
    print("Based on the design requirements this program has been generated "
          "as a template. Please edit def help() to replace this with your "
          "desired help information.")

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

