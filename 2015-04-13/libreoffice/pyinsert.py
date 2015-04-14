#!/usr/bin/env python3
# File: pyinsert.py
# Author: Ian Stewart
# Date: 2015-04-05
# Copyright:    This work is licensed under a Creative Commons 
#               Attribution-ShareAlike 4.0 International License.
#               http://creativecommons.org/licenses/by-sa/4.0/
#
# Repository: https://github.com/irsbugs
#             https://github.com/hampug
#
# Presentation: Prepared for the Hamilton Python User Group presentation 
#               held on 13 Apr 2015. 
#
# Notes: 
# 1. Use python3. Probably fails with python2 - not tested. 
# 2. Use Linux. Not designed for other platforms.
#
# Objective: 
# Convert a L.O. Application that uses python script in the User
# library, to having the python script embedded in the L.O. document file.
#
# Steps: 
# 1. Unzip LibreOffice documents files into a /tmp subdirectory.
# 2. Create in /tmp subdirectory the Scripts/python folders.
# 3. Copy python program from User library to /tmp/subdirectory/Scripts/python.
# 4. Into manifest.xml file insert the extra python folder and file names.
# 5. In the content.xml file, change the event-listeners to be in the document.
# 6. Re-zip the /tmp files back to a LibreOffice document. Minetype is first.

#TODO: Change the imports to try: / exception:
#TODO: Check its python v3.x
#TODO: Check its a Linux system and/or Support Windows
#TODO: Allow sub-folders and multiple python files.
#TODO: Add a tkinter GUI

__version__ = "1.0"

import sys
import os
import zipfile # For zipping and unzipping files.
import shutil 
# Use shutil.copy2 to preserve date of python file embedded in LibreOffice.
# Not necessary but could be handy for revision checking. 

# Constants / Assign variables
DEBUG_ON = False

def checkfile(path, filename):
    '''Check the path and filename are valid'''
    if os.path.isdir(path):
        if DEBUG_ON: print("{}\n...is a valid path".format(path))
        if os.path.isfile("{}".format(path + filename)):
            if DEBUG_ON: print("{}\n...is a valid file".format(
                                path + filename))        
            if os.access(path + filename, os.R_OK):
                if DEBUG_ON: print("{}\n...permits read access.".format(
                                    path + filename))      
            else:
                print("{} Read access not permitted".format(path + filename))                
        else:
            print("{} is an invalid file".format(path + filename))
    else:
        print("{} is an invalid path".format(path)) 

def unzip(path, filename, temp_directory):
    """
    Using the supplied path, unzip the LibreOffice file into the temporary
    directory. /tmp/lounzip
    """
    with zipfile.ZipFile(path + filename, "r") as z:
            z.extractall(temp_directory)
            
def rezip(temp_directory, pathnew, filenamenew):
    """
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
 
    # Walk the directory and retrieve a list of all paths and paths/filenames
    retrieve_list = []
    for root, dirs, files in os.walk(temp_directory, topdown=True):
        # Retrieve the paths    
        for dir_name in dirs:
            retrieve_list.extend([os.path.join(root, dir_name)])              
        # Retrieve  path and filename            
        for file_name in files:
            retrieve_list.extend([os.path.join(root, file_name)])
            
    if DEBUG_ON: 
        for item in retrieve_list:
            print(item)
    
    # Create an archive list with pairs of data. E.g.
    # ['/tmp/lounziped/mimetype', 'mimetype']
    # ['/tmp/lounziped/content.xml', 'content.xml']
    # item[0] is the source in /tmp folder. 
    # item[1] is the destination used in the zip archive
    archive_list = []                     
    for item in retrieve_list:
        # Remove the /tmp directory data from the start of item.
        output = item[len(temp_directory):] 
        archive_list.append([item, output])
    
    if DEBUG_ON: 
        for item in archive_list:    
            print(item) 
 
    # Shift mimetype to the front of the archive_list so it will be first
    # file written into the zip archive.
    for pointer, item in enumerate(archive_list):    
        if item[1] == 'mimetype':
            archive_list.insert(0, archive_list.pop(pointer))
          
    if DEBUG_ON: 
        for item in archive_list:    
            print(item) 
        
    # Use the archive_list to build the new libreoffice zip file
    # Opening as "w" removes previous version of file if it exists                     
    with zipfile.ZipFile(pathnew + filenamenew, 'w') as rezipfile:
        for item in archive_list: 
            rezipfile.write(item[0], item[1])

    # Clean up. Remove the files that were in /tmp
    shutil.rmtree(temp_directory)

def editmanifest(manpath, manfilename, pyfilename):
    '''
    Edit the /META-INF/manifest.xml file and insert Scripts, python and file.
    '''
    manifest_string1 = ('<manifest:file-entry manifest:full-path='
            '"Scripts/" manifest:media-type="application/binary"/>')

    manifest_string2 = ('<manifest:file-entry manifest:full-path='
            '"Scripts/python/" manifest:media-type="application/binary"/>')

    manifest_string3a = ('<manifest:file-entry manifest:full-path='
            '"Scripts/python/')
    manifest_string3b = pyfilename
    manifest_string3c = ('" manifest:media-type=""/>')

    identifier =  ('<manifest:file-entry manifest:full-path='
                    '"content.xml" manifest:media-type="text/xml"/>')

    # Rename the original manifest file.
    os.rename(manpath + manfilename, manpath + "manifest_original.xml")
    
    # Create a new manifest file and write original contents plus add the 
    # python related lines to the manifest
    with open(manpath + "manifest_original.xml", 'r') as infile, \
        open(manpath + manfilename, 'w') as outfile:
        for line in infile:
            outfile.write(line)
            #print(line)
            if identifier in line:
                #print("found identifier")            
                outfile.write("{}\n".format(manifest_string1,))
                outfile.write("{}\n".format(manifest_string2,))
                outfile.write("{}{}{}\n".format(manifest_string3a,
                    manifest_string3b, manifest_string3c))
                    
    # delete the original manifest file
    os.remove(manpath + "manifest_original.xml") 

def editcontent(contpath, contfilename):
    '''
    Change the content.xml file such that "location=user" is changed to 
    "location=document".
    contpath = temp_directory
    contfilename = "content.xml"      
    '''
    # Rename the original content.xml file.
    os.rename(contpath + contfilename, contpath + "content_original.xml")

    # Read content_original.xml to a string, preserve newline characters
    #with open(contpath + "content_original.xml", "r") as infile:
    with open(contpath + "content_original.xml", "r") as infile:    
        content_string = infile.read() #.replace('\n', '')
    
    # Split the string, based on space character, into a list.
    # Use split(" ") to preserve newline character, if any.
    content_list = content_string.split(" ")
    if DEBUG_ON: print("Content_list length: {}".format(len(content_list))) 
    # 549. with split(" ") is 548
    #print(content_list[2]) #<-- includes a newline character
    
    counter = 0
    for pointer, item in enumerate(content_list):
        #print(pointer,item)
        # 267 xlink:href="vnd.sun.star.script:pushbutton.py
        # $pushbutton?language=Python&amp;location=user"
        # List entries with ';location=user"' change to ';location=document"'
        if item.find(';location=user"') != -1:
            #print(item)          
            counter +=1
            item = item.replace(';location=user"',';location=document"')
            #print(item)
            content_list[pointer] = item
                        
    if DEBUG_ON: 
        print("'User' to 'document' changes performed: {}".format(counter))
        
    #for pointer, item in enumerate(content_list):
        #print(pointer,item)
        # Now changed to "location-document"  
        # 267 xlink:href="vnd.sun.star.script:pushbutton.py
        # $pushbutton?language=Python&amp;location=document"

    # Re-build the string
    content_string = " ".join(content_list)          
    #print(content_string)
    with open(contpath + contfilename, "w") as outfile:    
        #content_string = infile.read()        
        outfile.write(content_string)

    # delete the original content.xml file
    os.remove(contpath + "content_original.xml")
        
        
if __name__ == '__main__':
    '''
    Main Steps / Functions called:
    Assign values to string variables.
    Check the path and filaname to Original (user mode) LO file is valid
    Unzip LO document into a folder in /tmp/
    Create the directory in /tmp for Scripts/python
    Check can access the python program in user library
    Copy python program to /tmp Scripts/python
    Edit the manifest.xml file to contain the python folders and files.
    Edit the content.xml file to change eventlisteners from user to document
    Re-zip the /tmp and create new Open Doucment file.
    '''        
    # Initialize variables/constants
    # Working directory...
    temp_directory = "/tmp/lounziped/"
    # For libreoffice file to be modified to include embedded python program... 
    lopath = "/home/ian/pyuno for libreoffice/"
    lofilename = "pushbuttontimedoc.odg"
    lofilenamenew = "pushbuttontimedoc_embeddedpy.odg"    
    # For python program file...
    pypath = "/home/ian/.config/libreoffice/4/user/Scripts/python/"
    pyfilename = "pushbutton.py"    
    # For manifest file...
    manpath = temp_directory + "META-INF/"
    manfilename = "manifest.xml"
    # For content file...
    contpath = temp_directory
    contfilename = "content.xml"
    
    #checkfile("/home.pyuno for libreoffice/", "pushbuttontimedoc.odg")        
    checkfile(lopath, lofilename)            
    # unzip(path, filename, outfolder):
    unzip(lopath, lofilename, temp_directory)
            
    # Make the Scripts/python/ folder if it doesn't already exist'
    # os.makedirs(name, mode=0o777, exist_ok=False)
    # If exist_ok is False (the default), an OSError is raised if the target 
    # directory already exists.
    os.makedirs(temp_directory + "Scripts/python/", mode=0o777, exist_ok=True)


    
    # Copy pythonfile from User to /Scripts/python/ in unziped LO file in /tmp/
    # Check the python file
    checkfile(pypath, pyfilename)     
    # Copy python file
    shutil.copy2(pypath + pyfilename, temp_directory + "Scripts/python/")



    # Call the function to: 
    # Perform the editing of the manifest file
    editmanifest(manpath, manfilename, pyfilename)
 
    # Call function to:
    # Change the content.xml file such that "location=user" is changed to 
    # "location=document".
    editcontent(contpath, contfilename)
  
    #Re-zip the files in /tmp to make a new Open document file.
    rezip(temp_directory, lopath, lofilenamenew)

'''
NOTES:

    #print(os.curdir) # returns .
    
    
os.remove(path, *, dir_fd=None)

    Remove (delete) the file path. If path is a directory, OSError is raised. Use rmdir() to remove directories.
    
os.rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None)

    Rename the file or directory src to dst. If dst is a directory, OSError will be raised. On Unix, if dst exists and is a file, it will be replaced silently if the user has permission. The operation may fail on some Unix flavors if src and dst are on different filesystems. If successful, the renaming will be an atomic operation (this is a POSIX requirement). On Windows, if dst already exists, OSError will be raised even if it is a file.
    

Example of python code in manifest...
    
 <manifest:file-entry manifest:full-path="Scripts/python/Python/Hello1.py" manifest:media-type=""/>
 <manifest:file-entry manifest:full-path="Scripts/python/Hello.py" manifest:media-type=""/>
 <manifest:file-entry manifest:full-path="Scripts/python/" manifest:media-type="application/binary"/>
 <manifest:file-entry manifest:full-path="Scripts/" manifest:media-type="application/binary"/>    

===
    
 os.rmdir(path, *, dir_fd=None)

    Remove (delete) the directory path. Only works when the directory is empty, otherwise, OSError is raised. In order to remove whole directory trees, shutil.rmtree() can be used.    
===


os.curdir

    The constant string used by the operating system to refer to the current directory. This is '.' for Windows and POSIX. Also available via os.path.

===    
code]
#!/usr/bin/env python

import os, zipfile

def unzip(path, zip):
    isdir = os.path.isdir
    join = os.path.join
    norm = os.path.normpath
    split = os.path.split

    for each in zip.namelist():
        print each
        
    if not each.endswith('/'):

    root, name = split(each)

    directory = norm(join(path, root))

    if not isdir(directory):

    os.makedirs(directory)

    file(join(directory, name), 'wb').write(zip.read(each))

===

zip = zipfile.ZipFile('Python.zip', 'r')

unzip('', zip)

zip.close()
[/code]

===

Hexdump of a LO file. "PK" indicates its a PK-ZIP file.
First file is the mimetype, which in this .odg case, contains the ascii text.
application/vnd.oasis.opendocument.graphics

~/pyuno for libreoffice/==> hexdump -C pushbuttontime.odg
00000000  50 4b 03 04 14 00 00 08  00 00 bc ac 83 46 9f 03  |PK...........F..|
00000010  2e c4 2b 00 00 00 2b 00  00 00 08 00 00 00 6d 69  |..+...+.......mi|
00000020  6d 65 74 79 70 65 61 70  70 6c 69 63 61 74 69 6f  |metypeapplicatio|
00000030  6e 2f 76 6e 64 2e 6f 61  73 69 73 2e 6f 70 65 6e  |n/vnd.oasis.open|
00000040  64 6f 63 75 6d 65 6e 74  2e 67 72 61 70 68 69 63  |document.graphic|
00000050  73 50 4b 03 04 14 00 00  08 00 00 bc ac 83 46 b4  |sPK...........F.|
00000060  55 fe fd fc 73 00 00 fc  73 00 00 18 00 00 00 54  |U...s...s......T|
00000070  68 75 6d 62 6e 61 69 6c  73 2f 74 68 75 6d 62 6e  |humbnails/thumbn|
00000080  61 69 6c 2e 70 6e 67 89  50 4e 47 0d 0a 1a 0a 00  |ail.png.PNG.....|


No archive name so keeps the path name in the archive.
rezipfile.write(temp_directory + 'mimetype')
~/pyuno for libreoffice/==> hexdump -C pushbuttontimedoc_embeddedpy.odg
00000000  50 4b 03 04 14 00 00 00  00 00 64 7f 85 46 9f 03  |PK........d..F..|
00000010  2e c4 2b 00 00 00 2b 00  00 00 16 00 00 00 74 6d  |..+...+.......tm|
00000020  70 2f 6c 6f 75 6e 7a 69  70 65 64 2f 6d 69 6d 65  |p/lounziped/mime|
00000030  74 79 70 65 61 70 70 6c  69 63 61 74 69 6f 6e 2f  |typeapplication/|
00000040  76 6e 64 2e 6f 61 73 69  73 2e 6f 70 65 6e 64 6f  |vnd.oasis.opendo|
00000050  63 75 6d 65 6e 74 2e 67  72 61 70 68 69 63 73 50  |cument.graphicsP|
00000060  4b 01 02 14 03 14 00 00  00 00 00 64 7f 85 46 9f  |K..........d..F.|
00000070  03 2e c4 2b 00 00 00 2b  00 00 00 16 00 00 00 00  |...+...+........|
00000080  00 00 00 00 00 00 00 b4  81 00 00 00 00 74 6d 70  |.............tmp|
00000090  2f 6c 6f 75 6e 7a 69 70  65 64 2f 6d 69 6d 65 74  |/lounziped/mimet|
000000a0  79 70 65 50 4b 05 06 00  00 00 00 01 00 01 00 44  |ypePK..........D|


Replicates original OK when it has additional archive name parameter
rezipfile.write(temp_directory + 'mimetype', 'mimetype')
~/pyuno for libreoffice/==> hexdump -C pushbuttontimedoc_embeddedpy.odg
00000000  50 4b 03 04 14 00 00 00  00 00 90 82 85 46 9f 03  |PK...........F..|
00000010  2e c4 2b 00 00 00 2b 00  00 00 08 00 00 00 6d 69  |..+...+.......mi|
00000020  6d 65 74 79 70 65 61 70  70 6c 69 63 61 74 69 6f  |metypeapplicatio|
00000030  6e 2f 76 6e 64 2e 6f 61  73 69 73 2e 6f 70 65 6e  |n/vnd.oasis.open|
00000040  64 6f 63 75 6d 65 6e 74  2e 67 72 61 70 68 69 63  |document.graphic|
00000050  73 50 4b 01 02 14 03 14  00 00 00 00 00 90 82 85  |sPK.............|
00000060  46 9f 03 2e c4 2b 00 00  00 2b 00 00 00 08 00 00  |F....+...+......|
00000070  00 00 00 00 00 00 00 00  00 b4 81 00 00 00 00 6d  |...............m|
00000080  69 6d 65 74 79 70 65 50  4b 05 06 00 00 00 00 01  |imetypePK.......|
00000090  00 01 00 36 00 00 00 51  00 00 00 00 00           |...6...Q.....|


===

        # 'comment', 'compress_size', 'compress_type', 'create_system', 
        # 'create_version', 'date_time', 'external_attr', 'extra', 
        # 'extract_version', 'file_size', 'filename', 'flag_bits', 
        # 'header_offset', 'internal_attr', 'orig_filename', 'reserved', 
        # 'volume'
        
        
    with zipfile.ZipFile(pathnew + filenamenew, 'a') as rezipfile:
        print(zipfile.ZipFile.namelist(rezipfile)) # ['tmp/lounziped/mimetype']
        print(len(zipfile.ZipFile.infolist(rezipfile))) #1
        print(dir(zipfile.ZipFile.infolist(rezipfile)[0]))
        #print(zipfile.ZipFile.infolist(rezipfile)[0].filename)
        for item in zipfile.ZipFile.infolist(rezipfile):
            print (item.filename) # tmp/lounziped/mimetype
            print (item.date_time) # (2015, 4, 5, 16, 11, 58)
            print (item.compress_type) #0
            print (item.create_system) #3
            print (item.comment) # b''
            print (item.file_size) # 43 bytes
            print (item.orig_filename) # tmp/lounziped/mimetype
            print (item.header_offset) # 0
            print (item.create_version) # 20
            print (item.volume) # 0
            print (item.flag_bits) # 0
            print (item.internal_attr) # 0
    '''
