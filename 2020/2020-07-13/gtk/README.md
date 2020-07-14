# GTK Bits and Pieces

This presentation demonstrates aspects of GTK.

Please review the slide show for information on all the demos:

* gtk_presentation.odp
* gtk_presentation.pdf

## Image Embedding Tool

The [image-embedding-tool](https://github.com/HamPUG/meetings/tree/master/2020/2020-07-13/gtk/image-embedding-tool) produces
a base64 constants of an image. This constant may be embedded into a python GTK program.

## MessageDialog Function

The [dialog_demo](https://github.com/HamPUG/meetings/tree/master/2020/2020-07-13/gtk/dialog_demo) highlights the
MessageDialog() function. Normally this dialog will have buttons, like *OK* and *Cancel*. However the *Entry* widget
may be added to a dialog and on typing into the *Entry* widget, the *Enter* terminates the dialog frame and returns
the data that was entered.

## Constants, Enums and Flags

The [constants, enums and flags](https://github.com/HamPUG/meetings/tree/master/2020/2020-07-13/gtk/constants-enums-flags) contains a 
program that performs a `>>> dir(Gtk)` and analyzes the output. Two *.csv* files are created, so that you can review all the constants,
enums and flags that are available.
