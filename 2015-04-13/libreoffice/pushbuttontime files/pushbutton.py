# pushbutton.py
# Objective: To demonstrate python code with libreoffice.
# A libreoffice Draw or Writer or Cacl, etc. document contains a Button and a
# Textbox. Each time the button is pushed a message is displayed in the 
# Textbox. 
# 
# Pushbutton execute action: pushbutton.py$pushbutton (user, Python)

# Python's time and version number will be used to display in the textbox.
import time
import sys

# Function that main pushbutton is linked to and then executes the python code.
def pushbutton( event ):
    """Example of python code in libreoffice"""
    
    # Get the parent of the push button event and get the textbox of the parent
    textBoxModel = event.Source.getModel().getParent().TextBox1
    
    # Get existing text in the Textbox and output it to the Textbox with an
    # appended line of text with the current time and python version number.
    # 
    # Old text concatination method...
    #textBoxModel.Text = textBoxModel.Text + "\nPushed at: " + time.asctime() 
    # +  " Using Python: " + sys.version[:5]
    
    # Preferred python text formatting method
    textBoxModel.Text = ("{0}\nButton pushed: {1} using Python {2}"
        .format(textBoxModel.Text, time.asctime(), sys.version[:5]))        

def clear(event):
    """
    Clear the Textbox. 
    Pushbutton Execute Action: pushbutton.py$clear (user, Python)
    """
    textBoxModel = event.Source.getModel().getParent().TextBox1
    textBoxModel.Text = ""

    
def notes():

    """
    Example of an Error message. Created by not indenting this note.

    A Scripting Framework error occurred while running the Python script
    vnd.sun.star.script:pushbutton.py$pushbutton?language=Python&location=user.

    Message: <class 'IndentationError'>: 
    expected an indented block (pushbutton.py, line 52)

    /usr/lib/libreoffice/program/pythonscript.py:448 in function 
    getModuleByUrl() 
    [code = compile( src, encfile(uno.fileUrlToSystemPath( url ) ), "exec" )]

    /usr/lib/libreoffice/program/pythonscript.py:992 in function 
    getScript() 
    [mod = self.provCtx.getModuleByUrl( fileUri )]

    """
