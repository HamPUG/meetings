# view_pyc_file_3.7_up.py
# This will produce a disassembly of a .pyc file for python 3.7 and above.
# E.g. $ python view_pyc_file_3.7_up.py __pycache__/hello.cpython-310.pyc

import platform, time, sys, binascii, marshal, dis, struct

if sys.version_info.major == 3 and sys.version_info.minor < 7:
    sys.exit("For Python version 3.7 and above. Exiting...")


def view_pyc_file(path):
    """Read and display a content of the Python`s bytecode in a .pyc file."""
    with open(path, 'rb') as pyc_file:
        magic = pyc_file.read(4)
        bit_field = None
        timestamp = None
        hashstr = None
        size = None

        bit_field = int.from_bytes(pyc_file.read(4), byteorder=sys.byteorder)
        if 1 & bit_field == 1:
            hashstr = pyc_file.read(8)
        else:
            timestamp = pyc_file.read(4)
            size = pyc_file.read(4)
            size = struct.unpack('I', size)[0]
                
        code = marshal.load(pyc_file)


    magic = binascii.hexlify(magic).decode('utf-8')
    timestamp = time.asctime(time.localtime(struct.unpack('I', timestamp)[0]))

    dis.disassemble(code)

    print('-' * 80)
    print(
        'Python version: {}\nMagic code: {}\nTimestamp: {}\nSize: {}\nHash: {}\nBitfield: {}'
        .format(platform.python_version(), magic, timestamp, size, hashstr, bit_field)
    )
    
  
#===
    

#Code to display all op codes and op names
version = sys.version.split(" ")[0]
#print(version)
print("\nOpCodes for Python {} ByteCode".format(version))
op_name_dict = {}
for i in range(0,256): # max op code is 255.
    op_name = dis.opname[i]
    if op_name.startswith("<"):  # Unassigned opcodes display <255> etc.
        continue
    else:
        # Print op_code and its op_name
        print( "{:>3} {:>4}     {}".format(i, hex(i), op_name))
        op_name_dict[op_name] = i


# Sort op_name and display op_code 
print("\nOpNames for Python {} ByteCode".format(version))       
for key in sorted(op_name_dict):
    hex_value = hex(op_name_dict[key])
    hex_value = (hex_value[2:])
    if len(hex_value) < 2:
        hex_value = "0" + hex_value
    #print(hex_value)
    #print("{:<25}{:>3} {:>4}".format(key, op_name_dict[key], hex_value))
    # For pasting into a table.
    print("{} {} {}".format(key, op_name_dict[key], hex_value)) 


if __name__ == '__main__':
    view_pyc_file(sys.argv[1])
    sys.exit()
    
    
"""
References:

https://github.com/python/cpython

https://github.com/python/cpython/blob/main/Python/marshal.c

https://towardsdatascience.com/understanding-python-bytecode-e7edaae8734d

"""


