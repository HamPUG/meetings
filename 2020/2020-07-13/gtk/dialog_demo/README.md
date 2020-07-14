# MessageDialog Demo's

The **Gtk.MessageDialog()** is normally used to provide a message, like, *Are you finished?* and you click on *Yes* or *No*
buttons. Once a button has been clicked on, then the dialog frame is destroyed and the response of *Yes* or *No* is returned.

A variation is to include a **Gtk.Entry()** widget in the *MessageDialog* and remove any buttons. For example, you want 
a program to retrieve a *Password*. When the password has been typed in, then on typing the *Enter* key the password is
returned and the dialog frame is destroyed. This requires the *Entry* widgets callback, picking up the *Gtk.ResponseType.OK*.
This triggers the destruction of the dialog frame, and the text in the *Entry* is returned.

There are three demonstration files:

* dialog_demo.py
* dialog_demo_timeout.py
* dialog_demo_timeout_css.py

The program *dialog_demo.py* simulates requesting a Username and Password, whuke *dialog_demo_timeout.py* is a pop-up message 
that lasts for a random time and then the dialog frame is destroyed. 

The *MessageDialog* supports limited markup of the text field using tags, as follows:

* \<b>: Bold
* \<big>: Makes font relatively larger, equivalent to \<span size="larger">
* \<i>: Italic
* \<s>: Strikethrough
* \<sub>: Subscript
* \<sup>: Superscript
* \<small>: Makes font relatively smaller, equivalent to \<span size="smaller"> 
* \<tt>: Monospace
* \<u>: Underline
  
Also *MessageDialog* supports CSS. The program *dialog_demo_timeout.py* demonstrates markup, while *dialog_demo_timeout_css.py* demonstrates both markup and CSS. 
