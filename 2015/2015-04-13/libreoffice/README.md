LibreOffice and Python
======================

This folder includes the LibreOffice using Python presentation in *four* parts
and the `pyinsert.py` file.

*Part 4* of the Libreoffice using Python presentation highlights the use of the python program pyinsert.py.

Update for Version 2 of *Part 4*:

The Part 4 Version 2 presentation reflects changes that have been made to `pyinsert.py`. This modified file has now be named user2document.py. The changes include: 

1. Using a console command line interface to pass input and output files etc to the user2document.py program. This is done using the argparse module.
2. Using the module lxml to perform the modifications to the Manifest and Content xml files.

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

