#!/usr/bin/env python3
# -*- coding: utf-8 -*-
PROGRAM_NAME = "loadscript"
PROGRAM_INFO = "Load scripts to /usr/local/bin/"
PROGRAM_SPONSOR = ("""Hamilton Python User Group - https://github.com/HamPUG/
HamPUG is sponsored by Department of Computer Science
Waikato University. Hamilton, New Zealand.""")
PROGRAM_VERSION = "3.0"
DATE = "2015-09-14"
# Program:      loadscript.py
# Objective:    A utility to copy python files from development folders into.
#               /usr/local/bin so they may be run from the bash prompt.
# 
# Presention:   Hamilton Python User Group meeting 14 Sep 2015. 
#               https://github.com/HamPUG/
# Author:       Ian Stewart
# Date:         2015-09-14
# Portability:  Linux - Tested on Ubuntu 15.04
# Requires:     Python3 - Untested but will probably OK with python v2.7+
# Disk Access:  None
# Indentation:  Tabs
# Releases:
# V1.0. 2015-09-07
# V2.0. 2015-09-08 
# 	Correct wrong permissions on the files in /usr/local/bin.
#	(stat.S_IRWXU, stat.S_IRWXG, stat.S_IRWXO) #448+56+7=511 = 1FFh=777o
# V3.0. 2015-09-14
# 	Add -d --documentation as input argument.
#
# Import modules
import argparse
import sys
import os
import shutil
import stat
import time
from subprocess import Popen, PIPE
#
# Initialize constants / variables
DUMMY = " file not supplied "
HELP_MESSAGE_1 = "Script file to be copied to /usr/local/bin/"
HELP_MESSAGE_2 = "Display version number"
HELP_MESSAGE_3 = "Restore previous version of program - if it exists"
HELP_MESSAGE_4 = "Information on the version of the file in /usr/local/bin/"
HELP_MESSAGE_5 = "Documentation on use of loadscript program"
DOCUMENTATION = """
Description: 
loadscript is a python file residing in /usr/local/bin/ that will run from the 
linux command line prompt. It requires a input filename as an argument.

Actions that loadscript performs: 
    1. Copies a python or bash file (e.g. myprog_v3.py) to /usr/local/bin/ and
       renames by striping everything after the underscore, if it has one, or
       just strips the extension (e.g. myprog) 
    2. Any file in /usr/local/bin/ with the same name is renamed with an
       appended version, date stamp, and script type suffix. 
       (e.g. myprog_v1.3_2015-09-04.py3)
    3. Checks a file has a python or bash shebang. e.g. #!/usr/bin/env python3
    4. Changes the file to have execute status.
    5. Exit if failed to prefix command with sudo.
    6. List the file and any backed up copies it has in /usr/local/bin/
    7. Purge if more than three older files.
    8. Appending of version to backup files only if version found in script.
    9. Add a suffix of .py, or .py3 or .bash
   10. Undo. Remove existing /usr/local/bin/ and replace with previous 
       version, if it exists.
"""
def documentation():
	
	print("\nProgram: {} - {}".format(PROGRAM_NAME, PROGRAM_INFO))
	print()	
	print(PROGRAM_SPONSOR) 
	print(DOCUMENTATION)

def setup_argparse(parser):
	'''command line argument parsar'''
	parser.add_argument('input_file', nargs='?', type=str, help=HELP_MESSAGE_1,
						default=DUMMY)

	# Create a dummy file in /tmp/ so that input_file default parser will 
	# succeed when parameter is not actually passed.
	#DUMMY = "/tmp/tmp"
	#with open(DUMMY, 'w') as f: 
	#		f.closed		

	# The input_file is mandatory, but if missing then /tmp/tmp exists. 	
	#parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'),
	#					default=DUMMY, help=HELP_MESSAGE_1)
	# Namespace examples as a result of using type=argparse.FileType('r'):  
	# input_file=<_io.TextIOWrapper name='/tmp/tmp'  mode='r' encoding='UTF-8'>
	# input_file=<_io.TextIOWrapper name='fone_v1.py' mode='r' encoding='UTF-8'>

	parser.add_argument('-v','--version', action='version', help=HELP_MESSAGE_2, 
				version="Python Program: {}. Version: {}. Date: {}."
						.format(PROGRAM_NAME, PROGRAM_VERSION, DATE))

	parser.add_argument('-r', '--restore', help=HELP_MESSAGE_3,
					action='store_true', default=False)

	parser.add_argument('-i', '--info', help=HELP_MESSAGE_4,
					action='store_true', default=False)

	parser.add_argument('-d', '--documentation', help=HELP_MESSAGE_4,
					action='store_true', default=False)

	# https://docs.python.org/dev/library/argparse.html#action
	# ACTIONS: 'store' (default) 'store_const', 'store_true', 'store_false', 
	# 'count', 'append', 'append_const', 'version'
	#print(parser.parse_args())		
	return parser.parse_args() 

def check_permission():
	'''If not running with root permissions then exit'''
	if os.geteuid() != 0:
		sys.exit('Error: No permission. Use "sudo".')

def check_file_exists(input_file):
	'''Check the input file exists.'''
	if not os.path.isfile(input_file):
		return False
	return True

def check_valid_input_file(input_file):
	'''Check the input file is a valid file based on suffix.'''
	input_path_filename, input_extension = os.path.splitext(input_file)
	valid_extension = ['.py', '.py3', '.sh', '.bash']
	if input_extension not in valid_extension:
		sys.exit('Error: {} does not have a valid python / bash suffix.'
				.format(args.input_file))

def check_shebang(input_file):
	''' 
	Test the input file has a shebang and force syntax for portability.
	#!/usr/bin/env python Usually defaults to python 2.7.latest, and the 
	following defaults to 3.latest #!/usr/bin/env python3.
	Also support bash files with shebang of: #!/usr/bin/env bash
	'''
	shebang_list = (['#!/usr/bin/env python', '#!/usr/bin/env python3', 
					'#!/usr/bin/env bash'])
	with open(input_file) as f:
		shebang_line = f.readline()[:-1] # [:-1] strips newline character
		shebang_line = shebang_line.strip() # Strip any trailing spaces
		if shebang_line in shebang_list:
			return shebang_line.split(" ")[1] #python, python3 or bash

		else:
			print('Error: Shebang of "{}" is incorrect.\n'
					'The first line of the file must be either:'
					.format(shebang_line))
			for shebang_line in shebang_list:
				print(shebang_line)
			sys.exit('Exiting...')

def get_program_name(input_file):
	''' Seperate path and filename from the extension/suffix, then seperate 
	the filename from the path. 
	If filename has underscores, get text prior to first underscore
	e.g. "myprog_v3_2015-09-02.py" becomes "myprog"
	'''
	input_path_filename, input_extension = os.path.splitext(input_file)
	input_path, input_filename = os.path.split(input_path_filename)
	#print(input_path, input_filename)
	program_name = input_filename.rsplit("_")[0]
	#print(program_name)
	return program_name

def get_version(program_name):
	'''
	If the file already exists, search for any version numbering in the file.
	The version will be appended to the filename to aid in reviewing backups.   
	'''
	remove_chars = (['"', "'", '!', '@', '#', '$', '%', '^', '&', '*', '(',
					')', '+', '=',  '\\', '|', ';', ':', '[', ']',
					'{','}', '/', '?', ',', '<', '>', '`', '~'])
	version = ""
	if os.path.isfile('/usr/local/bin/{}'.format(program_name)):
		with open('/usr/local/bin/{}'.format(program_name)) as f:		
			for line in f.readlines():
				#print(line)
				if "version" in line.lower():				
					temp1 = line.lower().split("version")
					if temp1[1] != "":
						# split on "=" Version number should be after the =	
						if "=" in temp1[1]:
							temp2 = temp1[1].split("=")
							if temp2 != "":
								# should have the version number temp2[1]
								# strip spaces
								temp3 = temp2[1].strip()
								#print('|{}|'.format(temp3))
								# Get first part might be followed by commment
								temp4 = temp3.split(" ")
								temp5 = temp4[0]
								#print(temp5)
								# Use remove_chars list 								
								temp6 = ''.join(c for c in temp5 if not c in 
												remove_chars)	
								version = temp6							
								#print("Version:{}|".format(version))
								break 
	return version

def rename_old_file(program_name, version, script_type):
	'''
	Rename old file if it exists. Use copy not copy2. Copy2 preserves the
	original date and would prevent sort and purge.
	Append Version, data, and suffix. 
	Append .py, .py3 or .bash as suffix.
	E.g. myprog becomes myprog_v3_2015-09-06-112233.py3
	'''
	suffix_list = [['python', 'py'],['python3', 'py3'],['bash', 'bash']]	
	for item in suffix_list:
		if script_type == item[0]:
			suffix = item[1]

	if os.path.isfile('/usr/local/bin/{}'.format(program_name)):
		#print(time.strftime("%Y-%m-%d-%H%M%S", time.localtime()))
		'''		
		if version != "":		
			os.rename('/usr/local/bin/{}'.format(program_name), 
					'/usr/local/bin/{}_v{}_{}.{}'.format(program_name, version, 
					time.strftime("%Y-%m-%d-%H%M%S", time.localtime()), suffix))	
		else:
			os.rename('/usr/local/bin/{}'.format(program_name), 
					'/usr/local/bin/{}_{}.{}'.format(program_name, 
					time.strftime("%Y-%m-%d-%H%M%S", time.localtime()), suffix))
		'''
		# Dont use os.rename as we want the time meta of the shutil.copy		
		if version != "":		
			shutil.copy('/usr/local/bin/{}'.format(program_name), 
					'/usr/local/bin/{}_v{}_{}.{}'.format(program_name, version, 
					time.strftime("%Y-%m-%d-%H%M%S", time.localtime()), suffix))	
		else:
			shutil.copy('/usr/local/bin/{}'.format(program_name), 
					'/usr/local/bin/{}_{}.{}'.format(program_name, 
					time.strftime("%Y-%m-%d-%H%M%S", time.localtime()), suffix))

def copy_to_usrlocalbin(program_name):
	'''Copy input_file to /usr/local/bin/ and set as executable'''
	shutil.copy(args.input_file, ('/usr/local/bin/{}'.format(program_name)))
	print('{} is now in /usr/local/bin/'.format(program_name))
	os.chmod('/usr/local/bin/{}'.format(program_name), 
				stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO )
	#print(stat.S_IRWXU, stat.S_IRWXG, stat.S_IRWXO) #448+56+7=511 = 1FFh=777o

	# Set RWE for Owner, Group, Others.
	#st = os.stat(args.input_file) # Get values before the change so add.
	#os.chmod('/usr/local/bin/{}'.format(program_name), 
	#			st.st_mode | stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO )
	# Set RWE for Owner, Group, Others.

def list_and_purge(program_name):
	'''	
	List the file and last three versions of it, plus purge any older.
	Perform ls -t to get all files in /usr/local/bin sorted newest to oldest.
	'''
	print('Listing of {} files in /usr/local/bin/'.format(program_name)) 
	output = Popen(['ls', '/usr/local/bin', '-t',], stdout=PIPE)
	#print (output.stdout.read())
	count = 0
	for line in output.stdout.readlines():
		# convert byte stream to string and strip newline
		line  = line.decode("utf-8").rstrip("\n") 
	
		if program_name in line:
			count +=1 
			if count < 5:
				print(line) 	
			else:
				# Purge. Keep three older copies.
				os.remove('{}{}'.format('/usr/local/bin/', line))

def restore_previous_file(input_file):
	'''
	Restore the previous file. Read files from /usr/local/bin/ in date order.
	Newest date first. Thus second match is the file to be restored.
	'''	
	output = Popen(['ls', '/usr/local/bin', '-t',], stdout=PIPE)
	count = 0
	for line in output.stdout.readlines():
		# convert byte stream to string and strip newline
		line  = line.decode("utf-8").rstrip("\n") 
		#print(line[:len(input_file)])
		
		if input_file in line[:len(input_file)]:
			count +=1 
			if count == 2:
				print("File {} will be used to perform the restore."
					.format(line))
				# Remove the original file
				os.remove('{}{}'.format('/usr/local/bin/', input_file)) 
				# Use copy instead of rename			
				shutil.copy('/usr/local/bin/{}'.format(line), 
					'/usr/local/bin/{}'.format(input_file))
				# Remove the backup file.
				os.remove('{}{}'.format('/usr/local/bin/', line))
				break
	
			else:
				pass
		
	if count == 0:
		# No match for file
		print("Error: File {} is not in /usr/local/bin/".format(input_file))
		sys.exit()
	
	if count == 1:
		# No backups of the file exist
		print("Error: File {} has never been superceeded.".format(input_file))
		sys.exit()


if __name__ == '__main__':
	'''Launch loadscript'''
	parser = argparse.ArgumentParser(description='Move python and bash scripts '
			'to /usr/local/bin/', prefix_chars='-+/')
	args = setup_argparse(parser)

	if args.documentation:
		# No input_file required
		documentation()	
		sys.exit()

	if args.restore:
		'''Restore the previous version of the file, if it exists'''
		if args.input_file == DUMMY:
			sys.exit('Error: Provide a filename for a file in /usr/local/bin/')
		check_permission()
		restore_previous_file(args.input_file)		
		list_and_purge(args.input_file)
		sys.exit()

	if args.info:
		'''Provide information about the file in /usr/local/bin/'''
		# E.g. /usr/local/bin/cadence is a python3 script. Version: 4.0
		if args.input_file == DUMMY:
			sys.exit('Error: Provide a filename for a file in /usr/local/bin/')

		file_exists = check_file_exists('/usr/local/bin/{}'.format(args.input_file))
		if not file_exists:
			sys.exit('Error: /usr/local/bin/{} file does not exist.'
					.format(args.input_file))			
		else:		
			script_type = check_shebang("/usr/local/bin/{}".format(args.input_file))
			version = get_version(args.input_file)
			if version != "":			
				print('/usr/local/bin/{} is a {} script. Version: {}'
						.format(args.input_file, script_type, version))		
			else:
				print('/usr/local/bin/{} is a {} script. Version: unknown'
						.format(args.input_file, script_type))			
			sys.exit()

	#===== Start of default actions. Copying file to /usr/local/bin/ =====	
	# Exit if a filename is not provided.
	if args.input_file == DUMMY:
		sys.exit('Error: Provide a filename for a file in /usr/local/bin/')
	# Check if have sudo priv
	check_permission()

	# Check the file supplied args.input_file exists
	file_exists = check_file_exists(args.input_file)
	if not file_exists:
		sys.exit('Error: {} file does not exist.'.format(args.input_file))

	# Check the suffix/extension is valid. .py, .py3, .sh
	check_valid_input_file(args.input_file)

	# Test the input file has a shebang.
	# Return from the shebang whether python or bash script
	script_type = check_shebang(args.input_file)

	# Get the program name. e.g. myprog_v2.py --> myprog
	program_name = get_program_name(args.input_file)
	#print(program_name)

	# If file exists search if for a version=xxx and extract version number.
	version = get_version(program_name)
	
	# If file exists then rename it before copying new file.
	# test1 becomes test1_v1.4_2015-09-04-182520
	rename_old_file(program_name, version, script_type)

	copy_to_usrlocalbin(program_name)
	#print(args.input_file)

	list_and_purge(program_name)
	
sys.exit()

'''
Notes
###############################################################################
Examples of using loadscript

$ loadscript -h
usage: loadscript [-h] [-v] [-r] [-i] [-d] [input_file]

Move python and bash scripts to /usr/local/bin/

positional arguments:
  input_file           Script file to be copied to /usr/local/bin/

optional arguments:
  -h, --help           show this help message and exit
  -v, --version        Display version number
  -r, --restore        Restore previous version of program - if it exists
  -i, --info           Information on the version of the file in
                       /usr/local/bin/
  -d, --documentation  Information on the version of the file in
                       /usr/local/bin/
$
$ cat check_v1.py
#!/usr/bin/env python3
#
program_name = "check"
version = "1.0"
# 
print("Program name:{}. Version:{}".format(program_name, version))
$

$ sudo loadscript check_v1.py
check is now in /usr/local/bin/
Listing of check files in /usr/local/bin/
check

$ check
Program name:check. Version:1.0
$ loadscript -i check
/usr/local/bin/check is a python3 script. Version: 1.0

$ sudo loadscript check_v2.py
check is now in /usr/local/bin/
Listing of check files in /usr/local/bin/
check
check_v1.0_2015-09-16-122816.py3

$ sudo loadscript check_v3.py
check is now in /usr/local/bin/
Listing of check files in /usr/local/bin/
check
check_v2.0_2015-09-16-122822.py3
check_v1.0_2015-09-16-122816.py3

$ sudo loadscript check_v4.py
check is now in /usr/local/bin/
Listing of check files in /usr/local/bin/
check
check_v3.0_2015-09-16-122825.py3
check_v2.0_2015-09-16-122822.py3
check_v1.0_2015-09-16-122816.py3

$ sudo loadscript check_v5.py
check is now in /usr/local/bin/
Listing of check files in /usr/local/bin/
check
check_v4.0_2015-09-16-122828.py3
check_v3.0_2015-09-16-122825.py3
check_v2.0_2015-09-16-122822.py3
$ check
Program name:check. Version:5.0
$

$
$ sudo loadscript -r check
File check_v4.0_2015-09-16-122828.py3 will be used to perform the restore.
Listing of check files in /usr/local/bin/
check
check_v3.0_2015-09-16-122825.py3
check_v2.0_2015-09-16-122822.py3
$ check
Program name:check. Version:4.0
$

###############################################################################
Example: Using loadscript to update itself from V2.0 to V3.0
$ loadscript -i loadscript
/usr/local/bin/loadscript is a python3 script. Version: 2.0

$ sudo loadscript loadscript_v3.py
loadscript is now in /usr/local/bin/
Listing of loadscript files in /usr/local/bin/
loadscript
loadscript_v2.0_2015-09-16-110311.py3
loadscript_v1.1_2015-09-08-121300.py3

$ loadscript -i loadscript
/usr/local/bin/loadscript is a python3 script. Version: 3.0
$

###############################################################################
# Testing of the function for return of a version by reading the file...

def extract_version_from_line(version_line):
	remove_chars = (['"', "'", '!', '@', '#', '$', '%', '^', '&', '*', '(',
					')', '+', '=',  '\\', '|', ';', ':', '[', ']',
					'{','}', '/', '?', ',', '<', '>', '`', '~'])

	version = ''.join(c for c in version_line if not c in remove_chars)
	print('Version:{}|'format(version))

# Examples of the returns for checking the version
# This sentence contains the word version but has no equals sign.
# (Nothing)
# This sentence contains the word version and has an = sign in the line.
# Version:sign|
# __version__ = 1.2 # Comment
# Version:1.2|
# _version_ = 1.2.3.4
# Version:1.2.3.4|
# Version = 5F # Hex
# Version:5f|
# VERSION=1.2 # Stuff
# Version:1.2|
# VERSION = 1.3 Test
# Version:1.3|
# VERSION = "1'.'!@#$%^&*(){}[]|+:;"',\<>?/!5" Test
# Version:1.5|

# Using translate with python3
# temp6 = temp5.translate({ord('"'): '', ord('!'): '', ord("'"): ''})
###############################################################################
# stat modules constants:
# Permissions:
#S_IRUSR, S_IWUSR, S_IXUSR  Read, Write, Execute User
#S_IRGRP, S_IWGRP, S_IXGRP  RWE Group
#S_IROTH, S_IWOTH, S_IXOTH  RWE Other

#S_IREAD, S_IWRITE, S_IEXEC Same as Read, Write, Execute User. Unix 7 spec

# stat.S_IRWXU Mask for file owner permissions.
# stat.S_IRWXG Mask for group permissions.
# stat.S_IRWXO Mask for permissions for others (not in group).

#S_ISUID, Set UID bit.
#S_ISGID, Set-group-ID bit.  This bit has several special uses.
#S_ENFMT, System V file locking enforcement. 
#S_ISVTX, Sticky bit. A file in that directory can be renamed or deleted only 
#			by the owner of the file

# The #!/usr/bin/env python3 shebang means to execute using Python3 by 
# looking up the path to the Python interpreter automatically via env.
# http://stackoverflow.com/questions/10376206/what-is-the-preferred-bash-shebang/10383546#10383546

###############################################################################

'''
