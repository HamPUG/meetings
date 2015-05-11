# python_demo2.py
PYTHON_VERSION_MINIMUM = '3.5.0'
import sys
version_list = PYTHON_VERSION_MINIMUM.split(".")
version_minimum = 0
for i, x in enumerate(version_list):
    exponent =  abs((i - 3) * 8) # <== 24, 16, 8, 0
    version_minimum = version_minimum + int(x) * 2** exponent
if sys.hexversion < version_minimum: # 50659328 = 0x3050000 ~ 03.05.00.00
    sys.exit('The version of python being used is {}.'
             '\nThe minimum version of python for this application is {}.'
             '\nPlease upgrade the version of python.\nApplication {} '
             'terminated...'
             .format(sys.version.split()[0], PYTHON_VERSION_MINIMUM, 
                     sys.argv[0]))


    #print(x, version_minimum, exponent)
        #  3  50331648         24
        #  5  50659328         16
        #  0  50659328         8
#print(version_minimum) # 50659328
#print(hex(version_minimum)) # 0x3050000 ===> 03 05 00 00 ===> 3.5.0.0

