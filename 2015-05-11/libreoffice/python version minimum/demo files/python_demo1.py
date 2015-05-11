# python_demo1.py
PYTHON_VERSION_MINIMUM_STRING = '3.5.0'
PYTHON_VERSION_MINIMUM_HEX = 0x030500f0 # <== 03.05.00.f0 ~ 3.5.0.240
import sys
if sys.hexversion < PYTHON_VERSION_MINIMUM_HEX:
    sys.exit('The version of python being used is {}.'
             '\nThe minimum version of python for this application is {}.'
             '\nPlease upgrade the version of python.\nApplication {} '
             'terminated...'
             .format(sys.version.split()[0], PYTHON_VERSION_MINIMUM_STRING, 
                     sys.argv[0]))

# Note: f0 = final release. E.g. a0 = alpha release 0, b2 = beta release 2
