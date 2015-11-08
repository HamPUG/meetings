Python Universal Network Object (UNO) Bridge to LibreOffice/OpenOffice
======================================================================

Presentation at Hamilton Python User Group Meeting on 11 May 2015.

After installing the python uno bridge module, LibreOffice is launched with an
open communications port. An executing python script using the uno module, can
make a connection to the LibreOffice API and create documents or add content to
a document, etc. 

This Impress slide show has snippets of code from the pythonhouse.py example program.

To run the pythonhouse.py example program:

1. Install the python uno bridge module: 

```
sudo apt-get install python3-uno
```

2. Ensure that there are no libreoffice/openoffice applications running.

3. Open a terminal window and launch libreoffice with an open port command:

```
soffice "--accept=socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
```

4. Open another terminal window and run the example program:

```
python3 pythonhouse.py
```







