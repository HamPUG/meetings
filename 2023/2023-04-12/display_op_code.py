# Display all op codes and op names
import sys, dis

version = sys.version.split(" ")[0]
#print(version)
print("\nOpCodes for Python {} ByteCode".format(version))
op_name_dict = {}
for i in range(0,256): # max op code is 255.
    op_name = dis.opname[i]
    if op_name.startswith("<"):  # Unassigned opcodes display <255> etc.
        continue
    else:
        # Print op_code dec, op code hex, and op name
        print( "{:>3} {:>4}     {}".format(i, hex(i), op_name))
        op_name_dict[op_name] = i

# Sort op_name and display op name, op code dec and op code hex
print("\nOpNames for Python {} ByteCode".format(version))       
for key in sorted(op_name_dict):
    hex_value = hex(op_name_dict[key])
    hex_value = (hex_value[2:])
    if len(hex_value) < 2:
        hex_value = "0" + hex_value
    #print(hex_value)
    print("{:<25}{:>3} {:>4}".format(key, op_name_dict[key], hex_value))
    # For pasting into a table.        
    #print("{} {} {}".format(key, op_name_dict[key], hex_value)) 



