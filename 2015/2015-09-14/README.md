#### M#18

### Demostration of two python programs

Ian Stewart demonstrated two of his python programs. The programs are the 
files *loadscript.py* and *cadence_hampug_demo.py*.


#### loadscript.py

`loadscript.py` is designed to load a python script file or bash script file
from a current development folder and place it into `/usr/local/bin/` folder.
The files name will be truncated. For example, `myprog_v3.py` will become
`myprog`.

The permissions on the file copied to `/usr/local/bin` are modified, and the file
is checked to ensure it has a shebang in the first line. E.g. 
```bash
#!/usr/bin/env python3
```

The script may now be executed at the command line by just typing the file name
and providing any input options or arguments the program requires. E.g. 
```bash
$ myprog -i test.txt
```

Please see the 
```
$ loadscript --documentation
```
and the 
```
$ loadscript --help 
```
for more details.


#### cadence_hampug_demo.py

cadence is a command line program to model a bikes pedalling cadence to its
speed depending on what gears are used.

cadence features the generic function *query()* to solicit input from the User.
The *query()* function ensures the User types on the keyboard a response that is
acceptable to the desired data type of either string, boolean, integer or
floating point.

Type 
```bash
$ cadence_hampug_demo.py --help
```
for more information.

