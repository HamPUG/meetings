#!/usr/bin/env python3
#
# Manipulate "meetup-content-incrementing" file
import sys

"""
# This will pull the Date from meetup-content-increment file - for links
with open("meetup-content-increment", "r") as fin:
    buffer = []
    for line in fin.readlines():
        line = line[:-1]  # Remove the /n
        buffer.append(line)
        
        if len(buffer) < 5:
            continue
            
        else:           
            if buffer.pop(0).startswith("==="):
                s = "](" + buffer[1] + ")"
                print(s)        

sys.exit()
"""

"""
# This will pull the Date and the Title from meetup-content-increment file
with open("meetup-content-increment", "r") as fin:
    buffer = []
    for line in fin.readlines():
        line = line[:-1]  # Remove the /n
        buffer.append(line)
        
        if len(buffer) < 5:
            continue
            
        else:           
            if buffer.pop(0).startswith("==="):
                s = "* " + buffer[1] + "  **" + buffer[-1] + "**"
                print(s)        

sys.exit()
"""



# Get Date Title and Details. and format for .md file

fout = open("meetup-content-summary-increment.md", "w")

with open("meetup-content-increment", "r") as fin:
    buffer = []
    good_data = False
    count = 0
    count_1 = 0
    for line in fin.readlines():
        count_1 += 1
        line = line[:-1]  # Remove the /n

        if not line.startswith("==="):
            if good_data:
                buffer.append(line)        
            
        else:
            count += 1
            if len(buffer) > 0:
                buffer.pop(0)
                #buffer[0] = "## " + buffer[0]
                buffer[0] = "## [" + buffer[0] + "](" + buffer[0] + ")"

                buffer.pop(1)
                buffer[0] = buffer[0] + " " + buffer[1]
                buffer.pop(1)
                buffer.pop(1)
                

            print(buffer)
            for line in buffer:
                fout.write(line + "\n") 
            
            buffer = []
            good_data = True

        if line.startswith("Details"):
            buffer.pop()
            
        if line.startswith("Comments"): # or not line.startswith("==="): 
            buffer.pop()            
            good_data = False            
            
                
print(buffer)
for line in buffer:
    fout.write(line + "\n") 
fout.close()
                               
print(count) #  = 100


"""
# This will reverse the list. Changes year delimiter to same as month delimiter
with open("meetup-content-decrementing", "r") as fin:
    
    temp_buffer = []
    reverse_buffer = []
    
    delimiter_detected = False
    for line in fin.readlines():
        #print(line)
        
        if line.startswith("==="):
            if line == "======\n":
                line = "===\n"
            delimiter_detected = not delimiter_detected  # Toggle
                
        if delimiter_detected:
            temp_buffer.append(line)
    
        else:
            reverse_buffer = temp_buffer + reverse_buffer
            temp_buffer = []
            temp_buffer.append(line)
            delimiter_detected = not delimiter_detected  # Toggle

#print(reverse_buffer)
for item in reverse_buffer:
    #print(item)
    sys.stdout.write(item)
                    
with open("meetup-content-increment", "w") as fout:
    for item in reverse_buffer:
        fout.write(item)    
     
"""     
