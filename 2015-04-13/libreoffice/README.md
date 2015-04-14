LibreOffice and Python
======================

This folder includes the LibreOffice using Python presentation in *four* parts
and the `pyinsert.py` file.

*Part 4* of the Libreoffice using Python presentation highlights the use of the python program pyinsert.py.

The subfolder `pushbuttontimefile` contains files that were used/created as part of generating the LibreOffice using python presentation. As follows:

```
pushbuttontime.odg      <== Uses the User python macro library.
                            (Original program developed in User library)
pushbuttontimesys.odg   <== Uses the Shared python macro library
pushbuttontimedoc.odg   <== Uses the User python macro library
                            (Same as pushbuttontime.odg)
pushbuttontimedoc_embeddedpy.odg<== Uses the Document python macro library
                            (i.e. The python script is embedded in the .odg file)

pushbutton.py           <== python file with the functions pushbutton()
                            and clear(). Placed into User library:
                            ~/.config/libreoffice/4/user/Scripts/python/
                            ...and Shared library...
                            /usr/lib/libreoffice/share/Scripts/python/
                            ...and in the Document... 
                            /Scripts/python/
```

