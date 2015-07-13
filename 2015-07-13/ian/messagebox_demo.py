# messagebox_demo.py
# Program to demonstrate functionality of the tkinter.messagebox module
# https://github.com/HamPUG/
# Presentation for Hamilton Python User Group meeting - 2015 July 13
# Author: Ian Stewart

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

HELP_MESSAGE = """Help Information:
The tkinter.messagebox module calls the tkinter.commondialog import Dialog.

Importing (python3 syntax): 
from tkinter import messagebox

Example:
b_return = messagebox.showinfo("Messagebox Title", "This is the message")

tkinter.messagebox options:
showinfo, showwarning, showerror.
askquestion, askokcancel, askyesno, askyesnocancel, askretrycancel.

"""
class App:
    def __init__(self, root):
        self.root = root
        row,col = 0,0
        self.root.title("Demonstration of tkinter messagebox")
        self.labels = (["info", "warning", "error", "question", "proceed", 
                "yes/no","yes/no/cancel", "try again", "help", "Disabled"])

        self.buttons = []
        #self.buttons = ["dummy"]
        for index in range(10):

            self.buttons.append(ttk.Button(root, text=self.labels[index], 
                    width=15, command=lambda i=index:self.change(i)))

            self.buttons[-1].grid(row=row, column=col, ipadx=5, ipady=5, 
                    padx=5, pady=5)
            #  Grid parameters:
            #-column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, 
            #  -row, -rowspan, or -sticky

            col+=1
            if index%5==4: row+=1; col=0

        # Disable the 10th button. Not used
        self.buttons[9].config(state=DISABLED) # or state=NORMAL
       
        # Add a label
        self.info_label = ttk.Label(root, text="", background="white", 
                relief="sunken", font="FreeSans,20")

        self.info_label.grid(row=2, column=0, columnspan=5, ipadx=5, 
                ipady=5, padx=5, pady=5, sticky=(N, S, W, E))
         
         # Add a label2
        self.info_label2 = ttk.Label(root, text="", background="white", 
                relief="sunken", font="FreeSans,20")

        self.info_label2.grid(row=3, column=0, columnspan=5, ipadx=5, 
                ipady=5, padx=5, pady=5, sticky=(N, S, W, E))
		
    def change(self, index):
        # Clear the label for the return label        
        self.info_label.configure(text="")

        #==== Start of Simple, "OK" button only Messages" ====
        if self.buttons[index].configure("text")[4] == self.labels[0]:
            self.info_label2.configure(text='b_return = messagebox.showinfo'
                '("Messagebox", "showinfo.\\n\\nOne OK button.")')

            b_return = messagebox.showinfo("Messagebox", "showinfo."
                    "\n\nOne OK button. ")
            print("info", b_return)
            self.info_label.configure(text="Returned value: {}".
                format(b_return))

        if self.buttons[index].configure("text")[4] == self.labels[1]:
            self.info_label2.configure(text='b_return = messagebox.showwarning'
                '("Messagebox", "showwarning.\\n\\nOne OK button.")')

            b_return = messagebox.showwarning("Messagebox", "showwarning."
                    "\n\nOne OK button.")
            print("warning", b_return)
            self.info_label.configure(text="Returned value: {}".
                format(b_return))

        if self.buttons[index].configure("text")[4] == self.labels[2]:
            self.info_label2.configure(text='b_return = messagebox.showerror'
                '("Messagebox", "showerror.\\n\\nOne OK button.")')
            b_return = messagebox.showerror("Messagebox", "showerror."
                    "\n\nOne OK button.")
            print("error", b_return)
            self.info_label.configure(text="Returned value: {}".
                format(b_return))

        #==== End of Simple, "OK" Button Only Messages ====

        #==== Start of Multiple Button Messages" ====
        if self.buttons[index].configure("text")[4] == self.labels[3]:
            self.info_label2.configure(text='b_return = messagebox.askquestion'
                '("Messagebox", "Ask Question?\\n\\nYes or No buttons '
                'return yes or no")')
            b_return = messagebox.askquestion("Messagebox", "Ask Question?"
                    "\n\nYes or No buttons return yes or no")
            print("question", b_return)
            self.info_label.configure(text="Returned value: {}".
                format(b_return))

        if self.buttons[index].configure("text")[4] == self.labels[4]:
            self.info_label2.configure(text='b_return = messagebox.askokcancel'
                '("Messagebox", "Proceed?\\n\\nOK or Cancel buttons '
                'return True of False.")')
            b_return = messagebox.askokcancel("Messagebox", "Proceed?"
                    "\n\nOK or Cancel buttons return True of False.")
            print("proceed", b_return)
            self.info_label.configure(text="Returned value: {}".
                format(b_return))

        if self.buttons[index].configure("text")[4] == self.labels[5]:
            self.info_label2.configure(text='b_return = messagebox.askyesno'
                '("Messagebox", "Got it?\\n\\nYes or No buttons '
                'return True or False.")')            
            b_return = messagebox.askyesno("Messagebox", "Got it?"
                    "\n\nYes or No buttons return True or False.")
            print("yes/no", b_return)
            self.info_label.configure(text="Returned value: {}".
                format(b_return))

        if self.buttons[index].configure("text")[4] == self.labels[6]:
            self.info_label2.configure(text='b_return = messagebox.'
                'askyesnocancel("Messagebox", "Want it? \\n\\nYes, No or '
                'Cancel buttons return True False and None.")')
            b_return = messagebox.askyesnocancel("Messagebox", "Want it? "
                "\n\nYes, No or Cancel buttons return True False and None.")
            print("yes/no/cancel", b_return)
            self.info_label.configure(text="Returned value: {}".
                format(b_return))

        if self.buttons[index].configure("text")[4] == self.labels[7]:
            self.info_label2.configure(text='b_return = messagebox.'
                'askretrycancel("Messagebox", "Try Again?\\n\\nRetry or '
                'Cancel buttons return True or False.")')
            b_return = messagebox.askretrycancel("Messagebox", "Try Again?" 
                "\n\nRetry or Cancel buttons return True or False.")
            print("retry/cancel", b_return) 
            self.info_label.configure(text="Returned value: {}".
                format(b_return))

        #==== End of Multiple Button Messages" ====

        if self.buttons[index].configure("text")[4] == self.labels[8]:
            self.info_label2.configure(text='')
            self.info_label.configure(text=HELP_MESSAGE )
   
root = Tk()
app = App(root)
root.mainloop()


"""
Notes:

http://stackoverflow.com/questions/673174/file-dialogs-of-tkinter-in-python-3/673309#673309

The package Tkinter has been renamed to tkinter in Python 3, as well as other 
modules related to it. Here are the name changes:

    Tkinter → tkinter
    tkMessageBox → tkinter.messagebox
    tkColorChooser → tkinter.colorchooser
    tkFileDialog → tkinter.filedialog
    tkCommonDialog → tkinter.commondialog
    tkSimpleDialog → tkinter.simpledialog
    tkFont → tkinter.font
    Tkdnd → tkinter.dnd
    ScrolledText → tkinter.scrolledtext
    Tix → tkinter.tix
    ttk → tkinter.ttk

What are the differences between

    tkFileDialog → tkinter.filedialog
    tkCommonDialog → tkinter.commondialog
    tkSimpleDialog → tkinter.simpledialog


Also note that tkinter.filedialog is a module (not a class imported from a 
module). So, to get the class, you would do from tkinter.filedialog import 
FileDialog. There appears to be no plain FileDialog class in Python 2.x, 
though. Tell me if I'm wrong.

===

self.labels = ["info", "warning", "error", "question", "proceed", "yes/no",
"yes/no/cancel", "try again",]



$ python3 barray2.py
{'text': ('text', 'text', 'Text', '', 26), 
'width': ('width', 'width', 'Width', '', 1), 
'default': ('default', 'default', 'Default', <index object: 'normal'>, <index object: 'normal'>), 
'class': ('class', '', '', '', ''), 
'state': ('state', 'state', 'State', <index object: 'normal'>, <index object: 'normal'>), 
'compound': ('compound', 'compound', 'Compound', <index object: 'none'>, <index object: 'none'>), 
'image': ('image', 'image', 'Image', '', ''), 
'takefocus': ('takefocus', 'takeFocus', 'TakeFocus', 'ttk::takefocus', 'ttk::takefocus'),
'underline': ('underline', 'underline', 'Underline', -1, -1), 
'command': ('command', 'command', 'Command', '', <bytecode object: '140256251087304<lambda>'>), 
'cursor': ('cursor', 'cursor', 'Cursor', '', ''), 
'style': ('style', 'style', 'Style', '', ''), 
'textvariable': ('textvariable', 'textVariable', 'Variable', '', ''), 
'padding': ('padding', 'padding', 'Pad', '', '')}

===

ian@Aspire-5310-64Bit:~/tkinter$ python3 barray2.py
{'textvariable': ('textvariable', 'textVariable', 'Variable', '', ''), 
'image': ('image', 'image', 'Image', '', ''), 
'style': ('style', 'style', 'Style', '', ''), 
'borderwidth': ('borderwidth', 'borderWidth', 'BorderWidth', '', ''), 
'underline': ('underline', 'underline', 'Underline', -1, -1), 
'state': ('state', 'state', 'State', <index object: 'normal'>, <index object: 'normal'>), 
'anchor': ('anchor', 'anchor', 'Anchor', '', ''), 
'compound': ('compound', 'compound', 'Compound', <index object: 'none'>, <index object: 'none'>), 
'justify': ('justify', 'justify', 'Justify', '', ''), 
'class': ('class', '', '', '', ''), 
'cursor': ('cursor', 'cursor', 'Cursor', '', ''), 
'padding': ('padding', 'padding', 'Pad', '', ''), 
'text': ('text', 'text', 'Text', '', 'Name'), 
'relief': ('relief', 'relief', 'Relief', '', ''), 
'width': ('width', 'width', 'Width', '', ''), 
'font': ('font', 'font', 'Font', '', ''), 
'background': ('background', 'frameColor', 'FrameColor', '', ''), 
'takefocus': ('takefocus', 'takeFocus', 'TakeFocus', '', ''), 
'wraplength': ('wraplength', 'wrapLength', 'WrapLength', '', ''), 
'foreground': ('foreground', 'textColor', 'TextColor', '', '')}

"""
