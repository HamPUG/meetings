#!/usr/bin/env python3
#
# modify_notebook_metadata.py
#
# Modify the metadata of all markdown and code cells in a ipynb file so that 
# they may (or may not) can not be editable or deletable.
#
# Also provide a "restore" so that cells are reset to have no metadata.
#
# Ian Stewart
# 2019_08_02
#
import sys
import os
import shutil
import datetime
try:
    import simplejson as json
except ImportError:
    import json

heading = "\nModify ipynb files by changing the metadata of each cell. \n" \
    "Choose the modification option you wish to apply to the ipynb file(s):"      

# Initial status for modification of metadata
#          [ meta clear   markdown edit, code edit, mk deletble,  code del]
# status = [ False,       False,         False,     False,        False, ]

def get_action(status):
    """
    Query User as follows:
    1. Do they want to clear all cell metadata
    if not then
    2. Individually decide if the want cells markdown and code to be editable
    or deletable.
    Use a status list with 5 x True/False possibilities
    """
    while True:
        # clear metadata from all cells
        prompt = "Clear all cell metadata [N/y]: "
        response = input(prompt)
        if response == "": response = "n"
        if response.lower()[0] in ("n", "f", "0"):
            status[0] = False
        else:
            status[0] = True
        # Proceed?
        if status[0]:
            prompt = "Cell metadata will be cleared. Proceed? [Y/n]: "
            response = input(prompt)
        if response == "": response = "y"
        if response.lower()[0] in ("y", "t", "1"):
            return status
        else:
            pass

        # Editable
        prompt = "Set Markdown cell to be editable? [Y/n]: "
        response = input (prompt) 
        if response == "": response = "y"
        if response.lower()[0] in ("y", "t", "1"):
            status[1] = True  
        else:
            status[1] = False

        prompt = "Set Code cell to be editable? [Y/n]: "
        response = input (prompt) 
        if response == "": response = "y"
        if response.lower()[0] in ("y", "t", "1"):
            status[2] = True    
        else:
            status[2] = False

        # Deletable
        prompt = "Set Markdown cell to be deletable? [Y/n]: "
        response = input (prompt) 
        if response == "": response = "y"
        if response.lower()[0] in ("y", "t", "1"):
            status[3] = True   
        else:
            status[3] = False 

        prompt = "Set Code cell to be deletable? [Y/n]: "
        response = input (prompt) 
        if response == "": response = "y"
        if response.lower()[0] in ("y", "t", "1"): 
            status[4] = True  
        else:
            status[4] = False 
       
        # Proceed ?
        prompt = ("\nMarkdown cells: Editable:{} and Deletable:{}\n" \
                   "Code cells: Editable:{} and Deletable:{} \n" \
                    "Proceed? [Y/n]: "
                    .format(status[1], status[3], status[2], status[4]))     
        response = input(prompt)
        if response == "": response = "y"
        if response.lower()[0] in ("y", "t", "1"):
            return status
        else:
            continue


def get_ipynb_file_list():
    # In the current working directory get and display a list of opynb files.
    cwd = os.getcwd()
    file_list = sorted(os.listdir(cwd))
    # print(len(file_list))

    ipynb_list = []
    for index, file_name in enumerate(file_list):
        if file_name.split(".")[-1] == "ipynb":
            # print(file_name)
            ipynb_list.append(file_name)

    #print(ipynb_list, len(ipynb_list))
    print("\nIn the directory {}, there are {} ipynb files:"
            .format(cwd, len(ipynb_list)))
    for index, file_name in enumerate(ipynb_list):
        print("{:>3}. {}".format(index + 1, file_name))

    return ipynb_list


def select_files(ipynb_list):
    # Select which ipynb files to modify
    modify_list = []

    while True:
        prompt = "\nEnter the number of the file to modify or * for all files: "
        response = input(prompt)
        if response == "":
            print("Invalid response")
            continue
        if response == "*":
            print("Selected all files")
            modify_list = ipynb_list
            return modify_list

        try:
            response = int(response)
            if response < 1 or response > len(ipynb_list):
                print("Invalid file selected. Enter an integer between 1 and {}"
                    .format(len(ipynb_list)))
                continue
            else:
                print("The file selected is: {}".format(ipynb_list[response -1]))
                prompt = "Are you sure you want to modify this file? [Y/n]: "
                reply = input(prompt)
                if reply == "":
                    reply = "y"
                if reply.lower()[0] in ("y", "t", 1):
                    modify_list.append(ipynb_list[response -1])
                else:
                    continue

                prompt = "Are there more files you wish to modify? [N/y]: "
                reply = input(prompt)
                if reply == "":
                    reply = "n"
                if reply.lower()[0] in ["n", "f", 0]:
                    return modify_list
                else:
                    continue
        
        except ValueError as e:
            print("Value Error. Enter an integer between 1 and {}"
                    .format(len(ipynb_list)))
            continue


def create_backup_folder():
    # Make a backup folder to move files to before modification
    # folder format: backup-20190802-184512 
    time_str = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    folder = os.getcwd() + os.sep + "backup-" + time_str + os.sep
    #print(folder)
    os.mkdir(folder)
    print("A backup of the files before modification is in the folder:\n{}"
            .format(folder))
    return folder


def main():
    """
    Control the main flow of the program
    1. Get the ipynb files in the current working directory
    2. User selects the ipynb files to modify
    3. User selects which metatdata parameters to apply
    4. Create a backup folder to copy files to before modification
    5. If metadata to  be cleared then loop through for each file:
        o backup ipynb file to backup folder. 
        o open ipynb file as r+  
        o Use json module to load the file to data variable.
        o clear the metadata: data["cells"][i]['metadata'] = {}
        o fin.seek(0) # to reset file position to the beginning.
        o json.dump(data, fin, indent=1) # write data bck to file.
        o fin.truncate() # remove remaining part
    6. If metadata to be selectively modified perform steps in 5 except
        o instead of clear, set the desired parameter. For example:
            data["cells"][i]['metadata']['editable'] = True 
    """
    ipynb_list = get_ipynb_file_list()
    modify_list = select_files(ipynb_list)

    # Get User to decide on action to take.
    #          [ meta   mk edit cd edit mk del   code del]
    status = [ False, False,  False,  False,  False, ]
    status = get_action(status)
    #print(status)

    folder = create_backup_folder()

    if status[0]:
        print("\nClearing metadata of all cells in files:")
        for file_name in modify_list:    
            shutil.copy(file_name, folder + file_name)
            print(file_name)
            with open(file_name, "r+") as f:  
                data = json.load(f)
                total_cells = len(data["cells"])
                for i in range(total_cells):
                    data["cells"][i]['metadata'] = {}

                f.seek(0)  # reset file position to the beginning.
                json.dump(data, f, indent=1)
                f.truncate() # remove remaining part

        sys.exit("Completed clearing metadata on all cells.")

    else:
        # Setting matadata for each markdown and code cell.
        print("\nSetting metadata for ipynb files:")
        #print(status)
        for file_name in modify_list:
            shutil.copy(file_name, folder + file_name)
            print(file_name)
            with open(file_name, "r+") as f:  
                data = json.load(f)
                total_cells = len(data["cells"])
                for i in range(total_cells):
                    if data["cells"][i]['cell_type'] == "markdown":
                        data["cells"][i]['metadata']['editable'] = status[1]
                        data["cells"][i]['metadata']['deletable'] = status[3]
                    if data["cells"][i]['cell_type'] == "code":
                        data["cells"][i]['metadata']['editable'] = status[2]
                        data["cells"][i]['metadata']['deletable'] = status[4]
                f.seek(0)  # reset file position to the beginning.
                json.dump(data, f, indent=1)
                f.truncate()  # remove remaining part

        sys.exit("Completed setting metadata on cells.")

if __name__ == "__main__":

    if sys.version_info[0] != 3:
        sys.exit("Please use python version 3. Exiting...")

    print(heading)

    main()

"""
Cell metadata:
https://ipython.org/ipython-doc/dev/notebook/nbformat.html
The following metadata keys are defined at the cell level:
Key         Value 	        Interpretation
collapsed 	bool 	        Whether the cell’s output container should be 
                            collapsed
autoscroll 	bool or ‘auto’ 	Whether the cell’s output is scrolled, unscrolled, 
                            or autoscrolled
deletable 	bool 	        If False, prevent deletion of the cell
format 	    ‘mime/type’ 	The mime-type of a Raw NBConvert Cell
name 	    str 	        A name for the cell. Should be unique
tags 	    list of str 	A list of string tags on the cell. Commas are not 
                            allowed in a tag
Added with Jupyter version 5:
editable    bool    Can the cell be edited?
"""
