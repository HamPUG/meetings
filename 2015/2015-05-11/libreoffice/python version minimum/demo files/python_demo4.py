#python_demo4.py
PYTHON_VERSION_MINIMUM = '3.5.0' ; import sys
if sys.hexversion < sum([int(x) * 2**abs((i - 3) * 8) for i, x in enumerate
(PYTHON_VERSION_MINIMUM.split("."))]): sys.exit('The version of python being '
'used is {}.\nThe minimum version of python for this application is {}.'
'\nPlease upgrade the version of python.\nApplication {} terminated...'
.format(sys.version.split()[0], PYTHON_VERSION_MINIMUM, sys.argv[0]))
