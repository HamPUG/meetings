#!/usr/bin/env python3
#
# config_checker.py
#
# Checks if a .conf file exists for the program off 
# ~/.config/PROGRAM_NAME/PROGRAM_NAME.conf
# If not it creates one using INITIAL_DATA.
# Use Path from pathlib library https://docs.python.org/3/library/pathlib.html
#
# Ian Stewart - 2020-10-10

import sys
import os
from pathlib import Path

PROGRAM_NAME = Path(sys.argv[0]).stem
#print(PROGRAM_NAME)

def main(config):
    "Main program goes here"
    print("The main() part of the program is run...\n")
    print("Main program contains the following 'config' variable:\n{}"
            .format(config))


def check_conf_file():
    """
    Check if the local conf file exists at:
    ~/.config/PROGRAM_NAME/PROGRAM_NAME.conf
    """
    # Get the home path. These four all produce the same home variable.
    home = os.getenv("HOME")
    home = os.path.expanduser("~")
    home = str(Path.home())
    p = Path('~')
    home = str(p.expanduser())
    #print(home)

    CONF_PATH_FILE = (home + os.sep + ".config" +  os.sep + PROGRAM_NAME + 
            os.sep + PROGRAM_NAME + ".conf")
    #print(CONF_PATH_FILE)

    CONF_PATH = (home + os.sep + ".config" +  os.sep + PROGRAM_NAME + os.sep)
    #print(CONF_PATH)
    
    CONF_FILE = PROGRAM_NAME + ".conf" 
    #print(CONF_FILE)

    p = Path(CONF_PATH_FILE)
    if not p.exists():
        create_conf_file(CONF_PATH_FILE, CONF_PATH)
    
    return p.read_text()
    
    
def create_conf_file(path_file, path):
    "File, and maybe the path do not exist. Create path and file"
    print("Create path and conf file.")
    p = Path(path) 
    p.mkdir(parents=True, exist_ok=True) 
       
    p = Path(path_file)      
    p.write_text(INITIAL_DATA)

    # Playig with Pathlib methods...
    #print(p.stat())
    #print(p.owner())
    #print(p.group())

    #print(p.is_file())
    #print(p.exists())
    #p.touch(mode=0o666, exist_ok=True)
    #p.mkdir(mode=0o777, parents=True, exist_ok=True)     
    #p.touch(mode=0o666, exist_ok=True)     
    #print(p.read_text())
    #p.resolve(strict=False)  rmdir   


INITIAL_DATA = """Button_1, Waikato, Radio Waikato
Button_2, Concert, RNZ Concert Program
Button_3, Hauraki, Radio Hauraki
"""


if __name__ == "__main__":
    configuration = check_conf_file()
    main(configuration) 
    print("End of program") 
    
"""
Notes: From playing with Pathlib

p = Path(path) 
print(p.stat())

os.stat_result(
st_mode=33204, 
st_ino=263788, 
st_dev=2049, 
st_nlink=1, 
st_uid=1000, 
st_gid=1000, 
st_size=105, 
st_atime=1602306308, 
st_mtime=1602306308, 
st_ctime=1602306308
)

$ date --date='@1602306308'
Sat 10 Oct 2020 18:05:08 NZDT

print(p.owner())  # ian
print(p.group())  # ian

"""
          
