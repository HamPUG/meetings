#!/usr/bin/env python3
#
# File: user2document.py (Previously called: pyinsert.py)
# Author: Ian Stewart
# Date: 2015-05-12
# Copyright:    This work is licensed under a Creative Commons 
#               Attribution-ShareAlike 4.0 International License.
#               http://creativecommons.org/licenses/by-sa/4.0/
#
# Repository: https://github.com/irsbugs
#
# Notes: 
# 1. Use python3.2 or higher. Using os.makedirs 
# New in version 3.2: The exist_ok parameter.
# Changed in version 3.4.1: Before Python 3.4.1, if exist_ok was True and the 
# directory existed, makedirs() would still raise an error if mode did not 
# match the mode of the existing directory. Since this behavior was impossible 
# to implement safely, it was removed in Python 3.4.1. See issue 21082.
# versionchanged:: 3.3.6, 
#
# 2. Use Linux. Not designed for other platforms.
#
# Objective: 
# Convert a LibreOffice application that uses python scripts in a folder in 
# the LibreOffice python User library, to having the python scripts embedded 
# off a folder in the applications open document format (ODF) file. The 
# scripts are then stored in what is known as the "Document" python macro 
# library.
#
# Launching:    Launch from the command line interface. 
#               $ python3 user2document.py
#
# Steps: 
# 0. Select the file based on command line arguments. 
#       Input can be a single file or folder and all files in the folder.
#       Input defaults to a file in the User library.
# 1. Unzip LibreOffice documents files into a /tmp subdirectory.
# 2. Create in /tmp subdirectory the Scripts/python folders.
# 3. Copy python program from User library to /tmp/subdirectory/Scripts/python.
# 4. Into manifest.xml file insert the extra python folder and file names.
# 5. In the content.xml file, change the event-listeners to be in the document.
# 6. Re-zip the /tmp files back to a LibreOffice document. Minetype is first.

#TODO: Change the imports to try: / exception:
#TODO: Check its a Linux system / Support Windows
#TODO: Add a tkinter GUI
#TODO: Consider import pathlib and using PurePath to manipulate paths. V3.4 OK
#       https://pathlib.readthedocs.org/en/pep428/
# TODO: Use naming conventions: path, file, path_file, path_file_ext
# TODO: Enable appending of python files to .odf file. Rather than start clean
#  
#------------------------------------------------------------------------------
# Importing modules, defining variables and constants 
__version__ = "1.1"

import sys
import os
import argparse #parser = argparse.ArgumentParser()
import zipfile # For zipping and unzipping files.
import shutil # For copying files and deleting a tree of folders and files
# Use shutil.copy2 to preserve date of python file embedded in LibreOffice.
# Not necessary but could be handy for revision checking.
import glob # For collecting list of files in a wild-carded folder
import tempfile # For determining os platform temp folder
#import time # Can be used for debugging. E.g. time.sleep(10)
from lxml import etree
# Use lxml as python module for xml file manipulation. Has advantages over
# xml.etree.ElementTree. lmxl presereves namespaces. Doesn't convert to: ns0.
#
# Minimum version check. Examples of valid entries: 3, 3.4, 3.4.0, 3.4.0.f0 
# Version convention: '3.4.0.f0' = 50594032 = 0x30400f0 ==> 03.04.00.f0
PYTHON_VERSION_MIN = '3.2.0'
# 
version_minimum = sum([int(x, 16) * 2**abs((i - 3) * 8) for i, x in enumerate
                      (PYTHON_VERSION_MIN.split("."))])
if sys.hexversion < version_minimum:
    sys.exit('Python version      : {}.\nRequires Python     : {} or higher. ' 
             '\nExiting...'.format(sys.version.split()[0], PYTHON_VERSION_MIN))
#
# Constant assignment.                            
# Get PATH_TEMP that is platform independent 
# ie. Linux /tmp Windows c:\temp
# In development use /tmp. Later switch to self-removing
# odf_unzipped = tempfile.TemporaryDirectory('odf')
PATH_TEMP = ("{}{}{}{}".format(tempfile.gettempdir(), os.sep, "odf", os.sep))
#print(PATH_TEMP) # /tmp/odf/

# Later use the folloqwing code to create a temp dir
#with tempfile.TemporaryDirectory() as PATH_TEMP:
#    print(PATH_TEMP) # /tmp/tmppkusaebv

#CWD = os.getcwd() #/home/ian/.config/libreoffice/4/user/Scripts/python/utility
PATH_HOME = ('{}{}'.format(os.path.expanduser("~"), os.sep))
#print(HOME)  #/home/ian
PATH_USER_LIBRARY = ('{}{}'.format(PATH_HOME,
                        '.config/libreoffice/4/user/Scripts/python/'))
#print(PATH_USER_LIBRARY)
# /home/ian.config/libreoffice/4/user/Scripts/python/

# Valid filename extensions
EXTENSION = ('.py', '.py3')

# Replacement strings in content.xml
USER = 'location=user'
DOCUMENT = 'location=document'    

# Namespace for "manifest" used in mofiying the manifest.xml file. 
MANIFEST = '{urn:oasis:names:tc:opendocument:xmlns:manifest:1.0}'

HELP_MESSAGE_1 = '''File name or path and file name of python script in the 
LibreOffice User Library Scripts/Python repository. Examples: py_program.py 
or /py_path/py_program.py. Path must not start with a tilde. Example: ~/path/. 
The path may be single wildcarded * to select all Python Script files in 
that paths folder. Example: /py_path/* and the path may be double wildcarded
** or end with and ellipsis ... to select python files in the path and all 
sub-folders of the path. Example: /py_path/** /py_path/...
'''

HELP_MESSAGE_2 = '''ODF Document that will have python script inserted into it. 
Must reference a unique odf file. Encapsulate in quotes if folder or file 
names contain space characters. Wildcarding is not permitted. Example: 
~/Documents/"My Document.odt" '''

HELP_MESSAGE_3 = '''Supply a folder and filename for the created odf document 
that has had the python scripts embedded in it. Example: 
-o ~/Document/Doc_With_Python.odt. If the -o option is not used the filename 
has the same path as the original ODF file, but the file name is appended with 
"_embedded_python".
'''

HELP_MESSAGE_4 = '''Optional flag. Append to any python script that may 
already exist in the ODF Document. Otherwise existing python scripts will be
removed or overwitten.
'''

HELP_MESSAGE_5 = '''Optional flag. Increase output verbosity'''

HELP_MESSAGE_6 = '''Optional debug flag. Pauses the flow of the program to
allow inspection though another application of files in the /tmp folder. 
'''
#------------------------------------------------------------------------------
def setup_argparse(parser):
    '''1a-90
    Use argparse module to interpret the command line
    '''
    # User Library specific file or root folder containing python script(s)
    parser.add_argument('python_script', type=str, help=HELP_MESSAGE_1)
    
    # ODF Document file that will have the python scripts embedded in it.
    parser.add_argument('odf_document', type=str, help=HELP_MESSAGE_2)

    # Optional output file
    parser.add_argument('-o', '--output_file', type=str, help=HELP_MESSAGE_3)

    # Optional Flag to indicate if appending of python scripts should be
    # performed if the ODF document file aready contains python scripts.    
    parser.add_argument('-a', '--append', help=HELP_MESSAGE_4,
                        action='store_true')     
                            
    # Optional Verbosity - debug. See the following to implement
    # http://bip.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/argparse/
    #parser.add_argument('-v', '--verbose', action='count', default=0,
    #                    help=HELP_MESSAGE_5)

    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=HELP_MESSAGE_5)
                        
    parser.add_argument('-p', '--pause', help=HELP_MESSAGE_6,
                        action='store_true')
    
    args = parser.parse_args()  
    return args    
    # args.xxx are globally defined. No need to pass them to a function???
    #==== End of setting up argparse

def check_python_script_valid():
    '''1b1-50
    Test the python script argument to check if it is valid. 
    Invalid: Starts with ~/ or /home/ or // Ends with /
    Exit if invalid.
    '''
    #if args.verbose: print('\nF:args.python_script:')
    if args.verbose: 
        print('\nFunction            : check_python_script_valid()')
            
    if args.python_script[:2] == '{}{}'.format('~', os.sep):
        print('Error: May not commence python scripts selection with {}'
                .format('~', os.sep))
        sys.exit('Exiting...')

    elif args.python_script[:6] == '{}{}{}'.format(os.sep, 'home', os.sep):
        print('Error: May not commence python scripts selection with {}{}{}'
                .format(os.sep, 'home', os.sep))
        sys.exit('Exiting...')    

    elif args.python_script[:2] == '{}{}'.format(os.sep, os.sep):         
        print('Error: May not commence python scripts selection with {}'
                 .format(os.sep, os.sep))
        sys.exit('Exiting...')        
    #elif args.python_script[:1] == '{}'.format('.'):    
    #    print('Error: May not commence python scripts selection with {}'
    #             .format('.'))
    #    sys.exit('Exiting...')

    elif args.python_script[-1:] == '{}'.format(os.sep):       
        print('Error: May not end python scripts selection with {}'
                 .format(os.sep))
        sys.exit('Exiting...')  
    else:
        if args.verbose:   
            print('Information         : Python Scripts argument formed '        
                    'correctly.')
     
def build_full_path_file_string():
    '''1b2-50
    Build the full path and filename or wildcard string
    '''                  
    if args.verbose:   
        print('\nFunction            : build_full_path_file_string.')
         
    # Strip a leading seperator if it exists
    if args.verbose:   
        print('First character     : {}'.format(args.python_script[:1]))
        
    if args.python_script[:1] == os.sep:
        args.python_script = args.python_script[1:]
    
    if args.verbose:   
        print('args.python_script  : {}'.format(args.python_script))              
    # Join the Library and the python scripts string. Path.join adds seperator.
    python_script = os.path.join(PATH_USER_LIBRARY, args.python_script)

    if args.verbose:   
        print('python_script       : {}'.format(python_script))
        
    return python_script

def build_python_list(python_script):
    '''1b3-50
    Determine if argument ends in a wild card /* or /** or /...
    Of if it ends with a python file extension Eg. .py or .py3
    This function may call one of the following functions:
    get_python_file_folder(python_script)
    get_python_file_folder_all(python_script)
    get_python_file(python_script)
    '''
    if args.verbose:   
        print('\nFunction            : build_python_list(python_script)')    

    if python_script[-2:] == '{}{}'.format(os.sep, '*'):    
        #print('Argument ends with {}{} - Folder level file selection.'
        #         .format(os.sep, '*'))
        if args.verbose: print('Argument ends with  : '
                '{}{} Folder level file selection.'.format(os.sep, '*'))
                 
        python_script = python_script[:-1]  # strip *
        return get_python_file_folder(python_script)
                 
    elif python_script[-3:] == '{}{}'.format(os.sep, '**'):    
        #print('Argument ends with {}{} - Sub-folder level file selection.'
        #         .format(os.sep, '**'))
        if args.verbose: print('Argument ends with  : '
                '{}{} Sub-folder level file selection.'.format(os.sep, '**'))
        python_script = python_script[:-2]  # strip **
        return get_python_file_folder_all(python_script)        
        
    elif python_script[-4:] == '{}{}'.format(os.sep, '...'):    
        #print('Argument ends with {}{} - Sub-folder level file selection.'
        #         .format(os.sep, '...')) 
        if args.verbose: print('Argument ends with  : '
                '{}{} Sub-folder level file selection.'.format(os.sep, '...'))

        python_script = python_script[:-3]  # strip ...
        return get_python_file_folder_all(python_script)
                                    
    elif python_script[-3:] == '{}'.format('.py'):    
        #print('Argument ends with {} - File selection.'
        #         .format('.py'))
        if args.verbose: print('Argument ends with  : '
                '{}{} File selection.'.format(os.sep, '.py'))

        return get_python_file(python_script)                 
            
    elif python_script[-4:] == '{}'.format('.py3'):    
        #print('Argument ends with {} - File selection.'
        #         .format('.py3'))
        if args.verbose: print('Argument ends with  : '
                '{}{} File selection.'.format(os.sep, '.py3'))
        return get_python_file(python_script)         
                  
    else:
        print('Error: Python script argument {} is invalid.'
                 .format(python_script))                     
        sys.exit('Exiting...')
    
    if len(python_list) == 0:
        print('No files match {}'.format(python_script))
        sys.exit('Exiting...')


        #print('Total python files to copy to Document Library: {}'
        #        .format(len(python_list)))   
                    
    
def get_python_file_folder_all(path_wildcard):
    '''1b3a
    Get a list of all python files in supplied folder and all sub-folders.
    Called by function: build_python_list()
    '''
    if args.verbose:   
        print('\nFunction            : get_python_file_folder_all(path_wildcard)')
    # Use os.walk
    file_list = []
    for dirpath, dirnames, files in os.walk(path_wildcard):
        for item in files:
            # add to file_list the file with its directory path
            file_list.append(os.path.join(dirpath, item))               

    if args.verbose: print('Files in folders    : {}'.format(len(file_list)))
        
    file_list = [x for x in file_list if x.endswith(EXTENSION)]    
    return file_list 
        
        
def get_python_file_folder(path):
    '''1b3b
    Get a list of all python files in supplied folder
    Called by function: build_python_list()
    '''
    if args.verbose:   
        print('\nFunction            : get_python_file_folder(path)')
                    
    # glob.glob('/folder/*') only gets files in /folder/ and not subfolders.    
    file_list = [] 
    #python_pathfile_list[:] = []    
    file_list = glob.glob('{}{}'.format(path,'*'))
    # Ensure all files in the list end in .py or .py3
    # Use list comprehension method
    
    if args.verbose: print('Files in folder     : {}'.format(len(file_list)))

    file_list = [x for x in file_list if x.endswith(EXTENSION)]
    
    return file_list 
        
    # Note:
    # file_list = [x for x in file_list if x.endswith(EXTENSION)]
    # Above is list comprehension. Below does the same.
    # Use reverse list and pop off the list items that do not match extension
    #for position, item in reversed(list(enumerate(python_pathfile_list))):
    #    print(item)
    #    if not item.endswith(extension):
    #        python_pathfile_list.pop(position)
 
def get_python_file(path_file):
    '''1b3c
    Test string of one python file. If exists append to a list.
    Called by function: build_python_list()
    '''
    if args.verbose:
        print('\nFunction            : get_python_file(path_file)')
    file_list = []
    if os.path.isfile(path_file):
        file_list.append(path_file)
    return file_list

def checkfile(path, filename):
    '''1b4-20
    Check the path and filename are valid
    '''
    # TODO: re-write using pathlib. Path.exists(),Path.is_dir(),Path.is_file()
    # TODO: Remove this... Not necessary...
    if args.verbose:
        print('\nFunction            : checkfile(path, filename)')
        
    if os.path.isdir(path):
        if args.verbose: print('Valid path          : {}'.format(path))
        if os.path.isfile("{}{}".format(path, filename)):
            if args.verbose: print('Valid file          : {}{}'
                    .format(path, filename))
            if os.access(path + filename, os.R_OK):
                if args.verbose: print('Permits read access : {}{}'
                        .format(path, filename))                  
            else:
                print("{}{} Read access not permitted"
                        .format(path, filename))
                sys.exit('Exiting...')                
        else:
            print("{}{} is an invalid file".format(path, filename))
            sys.exit('Exiting...')             
    else:
        print("{} is an invalid path".format(path)) 
        sys.exit('Exiting...') 

def check_file_read_access(python_list):    
    '''1c
    Check each file in the python list has read access in User Library
    '''
    if args.verbose:
        print('\nFunction            : check_file_read_access(python_list)')

    # Strange it is OK with multiple seperators together? /folder//subfolder/x
    for item in python_list:
        #print(item)
        if not os.access(item, os.R_OK):
            print('Error: No read access to: \n{}'
                    .format(item))
            sys.exit('Exiting...')  

def process_output_file(odf_path, odf_filename):
    '''1e-90
    Process optional args.output_file argument. 
    Return the path and file name of new odf file to be created.
    Default is to append filename with _embedded_python 
    E.g. MyDocument.odg becomes MyDocument_embedded_python.odg
    Inputs: odf_path, odf_filename
    Return: odf_filename_new
    '''
    if args.output_file:
        # If path provided starts with ~/ then auto-translated to /home/user/
        # Otherwise prefix output file with the path of the odf file.
        if not args.output_file[:5] == '/home':
            # Check if provided filename starts with a path seperator.
            if args.output_file[:1] == os.sep:
                args.output_file = '{}{}'.format(odf_path, 
                        args.output_file[1:])
            else:
                args.output_file = '{}{}'.format(odf_path, args.output_file)
        try:
            # Test path and filename allow opening a file for write access
            f = open(args.output_file, "w")
            f.close()
            odf_filename_new = args.output_file
            #print(os.path.abspath(odf_filename_new))
        except:
            print('Unable to open output file: {}'.format(args.output_file))
            sys.exit('Exiting...')                    
    else:
        # Use the path, filename and extension of the odf file, but append 
        # filename with _embedded_python
        #odf_path, odf_filename
        file_pathname, file_extension = os.path.splitext(odf_filename)
        odf_filename_new = '{}{}{}{}'.format(odf_path, file_pathname, 
                '_embedded_python', file_extension)
        # print(os.path.abspath(odf_filename_new))          
    return odf_filename_new
    
def unzip(path, filename, temp_directory):
    """2-95
    Using the supplied path, unzip the LibreOffice file into the temporary
    directory. /tmp/odf/
    """
    if args.verbose: 
        print('\nFunction            : unzip(path, filename, temp_directory)')

    with zipfile.ZipFile(path + filename, "r") as z:
            z.extractall(temp_directory)
    #==== End of unzipping files to temp location =====
         
def copy_python_files(python_list):
    '''3-90
    Add the paths to temp location and copy the files to temp.            
    '''  
    if args.verbose: 
        print('\nFunction            : copy_python_files(python_list)')

    # Make the Scripts/python/ folder if it doesn't already exist'
    # os.makedirs(name, mode=0o777, exist_ok=False)
    # If exist_ok is False (the default), an OSError is raised if the target 
    # directory already exists.
    PATH_TEMP_PYTHON = '{}{}'.format(PATH_TEMP, 'Scripts/python/')
    if args.verbose: print('PATH_TEMP_PYTHON    : {}'.format(PATH_TEMP_PYTHON))    
    os.makedirs('{}'.format(PATH_TEMP_PYTHON), mode=0o777, exist_ok=True)
    
    # Strip the prefix off the start of the python_list files. Then append
    # suffix to PATH_TEMP_PYTHON. Append to temp_python_list
    temp_python_list = []
    for item in python_list:
        # Return the suffix in [1]. E.g. # messagebox/information/pythoninfo.py 
        # item_list.append(item.split(PATH_USER_LIBRARY)[1])

        # Contatinate the temp path with the suffix of the python_list
        # E.g. /tmp/odf/Scripts/python/messagebox/pythoninfo1.py 
        temp_python_list.append('{}{}'
            .format(PATH_TEMP_PYTHON, item.split(PATH_USER_LIBRARY)[1])) 
    
    #Create the directories off the tmp/odf/Scripts/python folder
    # head = /tmp/odf/Scripts/python/messagebox/information    
    # Prevents: FileNotFoundError: [Errno 2] No such file or directory:
    for item in temp_python_list: # item: messagebox/information/pythoninfo.py 
        head, tail = os.path.split(item)
        os.makedirs(head,  mode=0o777, exist_ok=True)

    if args.verbose: 
        print('Len:temp_python_list: {}'.format(len(temp_python_list)))

    # Copy python files from User Library (python_list)
    # to unziped odf file in /tmp/odf/Scripts/python (temp_python_list).    
    for pointer, item in enumerate(temp_python_list):
        shutil.copy2(python_list[pointer], temp_python_list[pointer])       

    if args.verbose: 
        print('Python files copied .')    
        for item in temp_python_list:
            print('                    : {}'.format(item))
    
    return temp_python_list
    # TODO: Use shutil.copytree? Does it build destination tree?
    # https://docs.python.org/3/library/shutil.html
    # copytree(source, destination, ignore=ignore_patterns('*.pyc', 'tmp*'))
    #==== End of copyin python files to temp folders =====

def modify_manifest(temp_python_list):
    '''4-95
    Append python path and filenames to the manifest file using lxml. 
    i.e. from lxml import etree.
    lxml preserves namspaces. E.g. Doesn't change 'manifest' to 'ns0'.
    An advantage of lxml module over xml.etree.ElementTree module.
    Namespace MANIFEST = '{urn:oasis:names:tc:opendocument:xmlns:manifest:1.0}'
    '''
    if args.verbose: 
        print('\nFunction            : modify_manifest(temp_python_list)')
    # Variable for path and filename of manifest file in temp directory
    manifest_pathfile = '{}{}'.format(PATH_TEMP, 'META-INF/manifest.xml')    
    if args.verbose: 
        print('manifest_pathfile   : {}'.format(manifest_pathfile))

    # Create a parser that removes any indentations that may already exist.
    xml_parser = etree.XMLParser(remove_blank_text=True)
    
    # Create tree using defined parser for easier to read layout in the file. 
    tree = etree.parse(manifest_pathfile, xml_parser)   
        
    root = tree.getroot()
    
    # Trim the PATH_TEMP prefix off the temp_python_list to create the 
    # manifest_python_list. E.g. Scripts/python/project/my_program.py
    manifest_python_list = []
    for item in temp_python_list: 
        manifest_python_list.append('{}'.format(item.split(PATH_TEMP)[1]))
                 
    if args.verbose:
        print('manifest_python_list.')        
        for item in manifest_python_list:
            print('                    : {}'.format(item))
         
    # Append elements to root for each python file path and filename
    # Ref: http://comments.gmane.org/gmane.comp.python.lxml.devel/3836     
    for path_filename in (manifest_python_list):
        root.append(etree.Element(('{}{}'.format(MANIFEST,'file-entry')), 
                attrib={
                ('{}{}'.format(MANIFEST,'full-path')) : path_filename, 
                ('{}{}'.format(MANIFEST,'media-type')) : 'text/xml'
                }))
                               
    # Overwrite manifest.xml with the modified xml tree
    # encoding='utf-8', xml_declaration=True inserts into the first line...
    # <?xml version='1.0' encoding='UTF-8'?>
    # ...not required under C14N specification. http://www.w3.org/TR/xml-c14n
    # In conjunction with initially using parser with indentation removal
    # use pretty_print to restore indentation when storing the file. 
    tree.write(manifest_pathfile, encoding='utf-8', xml_declaration=True, 
            pretty_print=True)
                  
    #==== End of modification to manifest.xml =====

def modify_content():
    '''5-90
    Perform modifications of the content.xml file.
    Change the content.xml file such that "location=user" is changed to 
    "location=document". Using lxml. i.e. from lxml import etree
    # Reference: http://lxml.de/xpathxslt.html#namespaces-and-prefixes
    # Replacement strings USER = 'location=user' DOCUMENT = 'location=document'
    '''  
    if args.verbose: print('\nFunction            : modify_content()')
    # Define the path and filename of file to be modified 
    content_pathfile = '{}{}'.format(PATH_TEMP, 'content.xml')
    if args.verbose: print('content_pathfile    : {}'.format(content_pathfile))
        
    # Create a parser to remove any indentations that may already exist
    xml_parser = etree.XMLParser(remove_blank_text=True)
    # Create tree using defined parser 
    tree = etree.parse(content_pathfile, xml_parser) 

    # Assign the root of the tree   
    root = tree.getroot() 

    # Locate using xpath the "event-listener" elements using namespaces.
    # The event-listener with "script" namespace, should have 4 x attributes. 
    # Two attributes use "xlink:href" and two use "script". 
    event_listener = root.xpath('//script:event-listener[@xlink:href]', 
            namespaces={
            'script':'urn:oasis:names:tc:opendocument:xmlns:script:1.0',
            'xlink':'http://www.w3.org/1999/xlink'})
    if args.verbose: 
        print('Len: event_listener : {}'.format(len(event_listener)))
                 
    # Iterate through the items of each event-listener. Each event-listener
    # item is a list of 4 x tuples containing key/value pairs. 
    # If the substring "location=user" is found in one of the values
    # replace it with "location=document". 
    # Set the new value using the key.
    # Event_listener requires an index. E.g. event_listener[i]
    counter = 0
    for i in range(len(event_listener)):
        for key, value in event_listener[i].items():
            if USER in value:
                value = value.replace(USER, DOCUMENT)
                event_listener[i].set(key, value)
                counter +=1
    if args.verbose: print('Changes: content.xml: {}'.format(counter))                
    # Over-write the tree back to the content.xml file.
    # Generate a version that gedit can display OK using pretty_print=True
    # Usiing pretty_print=True may impact performance.
    tree.write(content_pathfile, encoding='utf-8', xml_declaration=True, 
            pretty_print=True)    

    # Note: Looking at methods of event_listener[0], above could perhaps be 
    # done better with a find, or findtext, or iter or itertext...
    #print(dir(event_listener[0]))
    # 'addnext', 'addprevious', 'append', 'attrib', 'base', 'clear', 'extend', 
    # 'find', 'findall', 'findtext', 'get', 'getchildren', 'getiterator', 
    # 'getnext', 'getparent', 'getprevious', 'getroottree', 'index', 'insert', 
    # 'items', 'iter', 'iterancestors', 'iterchildren', 'iterdescendants', 
    # 'iterfind', 'itersiblings', 'itertext', 'keys', 'makeelement', 'nsmap', 
    # 'prefix', 'remove', 'replace', 'set', 'sourceline', 'tag', 'tail', 
    # 'text', 'values', 'xpath'
    
    #===== End of modification of content.xml
    
def rezip(temp_directory, pathnew, filenamenew):
    """6-95
    Using the supplied path into /tmp, rezip the LibreOffice files. 
    The mimetype file contains text like this: 
    application/vnd.oasis.opendocument.graphics
    The minetype file must be the first file in the zipped libreoffice 
    document. 
    The libreoffice document should have the same extension as the original.
    E.g. .odt for writer, .ods for calc, .odp for impress, .odg for draw, etc. 
    Place the zipped file in the same directory as original LO document,
    but with appended filename. E.g. xxx_embeddedpy.odg
    Remove all files in /tmp
    """
 
    if args.verbose: print('\nFunction            : rezip(temp_directory, '
            'pathnew, filenamenew)') 
    # Walk the directory and retrieve a list of all paths and paths/filenames
    retrieve_list = []
    for root, dirs, files in os.walk(temp_directory, topdown=True):
        # Retrieve the paths    
        for dir_name in dirs:
            retrieve_list.extend([os.path.join(root, dir_name)])              
        # Retrieve  path and filename            
        for file_name in files:
            retrieve_list.extend([os.path.join(root, file_name)])

    if args.verbose: 
        print('retrieve_list       .')            
        for item in retrieve_list:
            print('                    : {}'.format(item))
    
    # Create an archive list with pairs of data. E.g.
    # ['/tmp/odf/mimetype', 'mimetype']
    # ['/tmp/odf/content.xml', 'content.xml']
    # item[0] is the source in /tmp folder. 
    # item[1] is the destination used in the zip archive
    archive_list = []                     
    for item in retrieve_list:
        # Remove the /tmp directory data from the start of item.
        output = item[len(temp_directory):] 
        archive_list.append([item, output]) 
 
    # Shift mimetype to the front of the archive_list so it will be first
    # file written into the zip archive.
    for pointer, item in enumerate(archive_list):    
        if item[1] == 'mimetype':
            archive_list.insert(0, archive_list.pop(pointer))
          
    if args.verbose: 
        print('archive_list item[1].')
        for item in archive_list:    
            print('                    : {}'.format(item[1])) 
       
    # Use the archive_list to build the new libreoffice zip file
    # Opening as "w" removes previous version of file if it exists                     
    #with zipfile.ZipFile(pathnew + filenamenew, 'w') as rezipfile:
    with zipfile.ZipFile(filenamenew, 'w') as rezipfile:

        for item in archive_list: 
            rezipfile.write(item[0], item[1])

    # Clean up. Remove the files that were in /tmp
    shutil.rmtree(temp_directory)   
    #===== End of re-zipping temp files to create new ODF file        
#------------------------------------------------------------------------------
if __name__ == '__main__':
    '''
    Main Steps / Functions called:
    1. Setup / Initialization section:
    1a. Setup Argument Parser
    1b. Interpret python_script argument. Create a list of python files 
    1c. Call function to test there is read access to each file in User library
    1d. Interpret odf input file argument    
    1e. Process argument for output file containing embedded python
    1f. Optional --append argument - Not Implemented
    1g. Create a clean tempdirectory
    
    2. Unzip the ODF file to a temp folder    
    3. Add the paths and copy the files to temp
    4. Append python files paths and filenames to manifest.xml file
    5. Perform modifications to content.xml. Change from "user" to "document"
    6. Re-zip the files in /tmp and make new odf file.     
    '''
                  
    #1a=== Call function to setup the argument parser      
    parser = argparse.ArgumentParser()
    args = setup_argparse(parser)
    if args.verbose: 
        print()
        print('Program             : {}'.format(sys.argv[0]))
        print('Version             : {}'.format(__version__))
        print('Python version      : {}'.format(sys.version.split()[0]))
        print('hex(sys.hexversion) : {}'.format(hex(sys.hexversion)))        
        print('PATH_USER_LIBRARY   : {}'.format(PATH_USER_LIBRARY))    
        print('PATH_HOME           : {}'.format(PATH_HOME))
        print('PATH_TEMP           : {}'.format(PATH_TEMP))     
        print('args.python_script  : {}'.format(args.python_script))
        print('args.odf_document   : {}'.format(args.odf_document))
        print('args.output_file    : {}'.format(args.output_file))    
        
    # The following does not translate args.python_script ...(strange?)...
    #print('{0:<30}: {0:}'.format('args.python_script', args.python_script            
    #print(OUTPUT_FILE) #<--Strange. In --help it looks like its env variable.

    #1b=== Interpret args.python_script argument. Create a list of python files        
    # A file of folder off the Libreoffice User library/Scripts/python/
    # Rules for Python script argument:
    # Can not start with a ~/ or a . or // Note: Bash converts ~/ to /home/
    # Can not start with quoted ~/ E.g. "~/folder/*" parsed as ~/folder/*
    # Can not end with /
    # Ends in .py then argument refers to a single file or path and single file
    # Start with / and ends in a /* then argument is the files in a folder.
    # Start with / and ends in /** then argument is files in folder and all
    #   subfolders.
    # Is only a * then argument is the files in User Library root directory
    # Is only ** then argument is all files in User Library.
    #
    # Reject illegally formed argument. Starting with ~/ . // or end with /
    # Unable to pass string args.python_script with a . in it.
    
    # Convert argument to string variable so it can be passed to a function 
    argument_python_script = args.python_script
    
    # Function: check there is no illegal syntax in the python_script argument.
    check_python_script_valid()
    
    # Function: Prefix the path with User Library path and Scripts/python
    python_script = build_full_path_file_string()
    
    # Determine if argument ends in a wild card /* or /** or /...
    # Or if it ends with a python file extension Eg. .py or .py3
    # Function: Return a list containing only files with valid EXTENSION's.  
    python_list = build_python_list(python_script)
    if args.verbose: 
        print('Total python files  : {}'.format(len(python_list)))

    #1c=== Call function to test there is read access to each file. 
    # Probably unnecessary, but better to have an error now than an error later 
    check_file_read_access(python_list)
    
    #1d=== Process argument for path and filename of odf document =====
    # args.odf_document
    # Must be a single file. Will over-write existing file.
    # File can be prefixed with ~/ or /folder/ 
    # If args.odf_document is wildcard and a list is returned then command
    # line error: unrecognized arguments.
    # 
    # Split the path and the filename
    odf_path, odf_filename = os.path.split('{}'.format(args.odf_document))
     
    if args.verbose: 
        print('odf_filename        : {}'.format(odf_filename))
        print('odf_path            : {}'.format(odf_path))
        print('o.s. seperator      : {}'.format(os.sep))
        print('python_script       : {}'.format(python_script))
        print('current working dir : {}'.format(os.getcwd()))
    
    # If there is no filename then exit
    if len(odf_filename) == 0:
        print('odf file not provided')
        sys.exit("Exiting...")
 
    # if path is prefixed with ~/ then automatically converted to /home/user/
    # if not beginning with /home, prefix with the current working directory.
    # Append a seperator to the path.
    if not odf_path[0:5] == '/home':  # Will be /home if ~/ prefix to path
        # Prefix path with current working directory and append seperator
        odf_path = ('{}{}{}'.format(os.getcwd(), odf_path, os.sep))
    else:
        # Append the os.seperator
        odf_path = ('{}{}'.format(odf_path, os.sep))
         
    if args.verbose: print('updated odf_path    : {}'.format(odf_path))
        
    # Test path and filename exist....
    checkfile(odf_path, odf_filename)     
       
    #1e=== Call function to process args.output_file path and filename =====
    # Optional argument. Default is to append filename _embedded_python.
    # E.g. MyDocument.odt becomes MyDocument_embedded_python.odt
    odf_filename_new = process_output_file(odf_path, odf_filename)

    #1f=== Optional --append argument - Not Implemented
    # Set Constant to determine if exisiting python scripts in the document
    # are to be preserved or stripped and replaced.
    # 
    #if args.append:
    #    print("optional -a or --append was detected")
    #    STRIP_EXISTING_SCRIPT = True
    #else:
    #    print("No optional -a or --append detected")
    #    STRIP_EXISTING_SCRIPT = False

    #1g=== Create a clean tempdirectory for the document in unzipped form.
    # Use a non-autoremoving temp dir during development.
    # If temp directory exists remove it and any files that might be in it.
    if os.path.exists(PATH_TEMP): 
        shutil.rmtree(PATH_TEMP)
    # Create a new temp directory.
    if not os.path.exists(PATH_TEMP):
        os.makedirs(PATH_TEMP) 
    
    #2==== Call function to unzip the ODF file to a temp folder
    # unzip(input path, input filename, output folder for unzipped files):
    unzip(odf_path, odf_filename, PATH_TEMP)
    if args.pause: 
        input("\nODF unzipped        : Next - Copy python files [continue]")

    #3==== Call function add the paths and copy the files to temp
    # Return temp_python_list for use in modifying manifest.xml file
    temp_python_list = copy_python_files(python_list)
    if args.pause: 
        input("\nPython copy in temp : Next - manifest.xml. [continue]")
    
    #4==== Call function to append path and filenames to manifest.xml
    modify_manifest(temp_python_list)
    if args.pause: 
        input("\nManifest.xml append : Next - content.xml. [continue]")    

    #5==== Call function to perform modifications to content.xml
    modify_content()
    if args.pause:
                 
        input("\nContent.xml modified: Next - rezip temp files [continue]")    

    #6==== Call function to Re-zip the files in /tmp and make new odf file.
    rezip(PATH_TEMP, odf_path, odf_filename_new)
    
    head, tail = os.path.split(odf_filename_new)
    print('\nCompleted embedding : New libreoffice document is located...')
    print('odf python file path: {}{}'.format(head, os.sep)) 
    print('odf python file name: {}'.format(tail))       
    if args.verbose:    
        print('Finished            :\n')


