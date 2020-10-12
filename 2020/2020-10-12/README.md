

# Demonstration Programs

Ian demonstrated two small programs that highlight some functions he had written. These functions could be incorporated in a Python program you are writing and be called at the beginning of a python program. The programs demonstated were:

* config_checker.py
* program_update.py


## config_checker.py

Many programs require a default set of local parameters in order to run. Later these parameters may be tailored by the User to suit the needs of the User. These parameters are normally stored in a configuration file. On Linux systems the configuration file (.conf) is normally in the path:

/home/USER/.config/PROGRAM_NAME/PROGRAM_NAME.conf

Thus in this case where the User is Ian and the program name is config_checker.py, then the configuration file would be located in:

/home/ian/.config/config_checker/config_checker.conf

If, for example, the program was for listening to internet radio stations, then my program might be called radio.py and its configuration file would be located in:

/home/ian/.config/radio/radio.conf

In the case of radio.conf the contents of the file could be to set up three radio stations that are your favourites. These radio stations would then be selected by clicking on one of three buttons in the programs GUI. Thus the contents of the conf file might be:

Button_1, Waikato, Radio Waikato
Button_2, Concert, RNZ Concert Program
Button_3, Hauraki, Radio Hauraki

Thus the program begins by calling the function check_conf_file():

configuration = check_conf_file()

This function checks for the existance of a configuration file. 

If it does not exist then create_conf_file function is called and the path and .conf file are created and the initial data is placed into the file. 

The conf file is read and its contents are returned from the function. The main() function of the programm may then be launched and it passes the configuration.

This program utilises Path from the pathlib library. For example, "Path.read_text()" is used in place of "with open(file, "r") as fin".


## program_update.py

This program is a simple attempt at self modifying code. The last line of the program is a comment delimiter followed by a number. The initial number is zero. Each time the program is run the number is incremented by one and the program is re-written with this updated number. Thus a built-in count of the number of times the program has been run is kept.


## Pathlib source code

https://github.com/python/cpython/blob/master/Lib/pathlib.py

The class "Path" begins at line 1055.

An example of the Path.read_text() code....

    def read_text(self, encoding=None, errors=None):
        """
        Open the file in text mode, read it, and close the file.
        """
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
            return f.read()
            

Pathlib documentation is here:
 
https://docs.python.org/3/library/pathlib.html
