# Constant

Ian Stewart delivered a presentation on the use of constants when a program is launched to set the desired parameters for the program.

There was discussion at the meeting on how safe it is to use eval() and exec() functions. It is possible that the configuration file that the User has the priv to edit, could be maliciously modified. This editing could result in corrupting the flow of the main program that has read the configuration file, or delivering damage to the file system, etc.

Attached are two files:
* **main_program.py**
* **constant.conf**

These two files may be downloaded to a folder and you can perform multiple runs of main_program.py while editing constant.conf to see if you can introduce malicious code via constant.conf.


Summary of checks performed on each line from constant.conf:

* constant.conf exists, if not ignore that its not avaialble.
* Strip line of whitespace at start and end
* Ignore the line if it starts with a comment, i.e. #
* Split the line based on " = " being the only valid assigning for a constant.
* Ignore the line if split did not return a list of two items.

* Perform checks on the namespace of the constant:
  *  Strip any whitespace
  *  Ignore the line if it starts with an underscore. i.e. System constant.     
  *  Ignore the line is there are spaces in the name
  *  Ignore the line if constant identifier is not all uppercase, but allow _

* Perform checks on the literal assigned to the constant:
  *  Strip literal of any whitespace.
  *  Check if literal is of a supported data type in _SUPPORTED_TYPE_LIST
  *  If literal is a string then check _SPACES_IN_STRING bool is applicable.

If the line has made it through the above checks then execute the code in the line and
modify a constant that the main section of code will make use of.

Also keep a count of each constant that is modified. Apply the limit on how many
constants may be modified.


