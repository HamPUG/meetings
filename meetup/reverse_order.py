import sys

# This will reverse the list. Changes year delimiter to same as month delimiter
with open("meetup_content_decending", "r") as fin:
    
    temp_buffer = []
    reverse_buffer = []
    
    delimiter_detected = False
    for line in fin.readlines():
        #print(line)
        
        if line.startswith("==="):
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

