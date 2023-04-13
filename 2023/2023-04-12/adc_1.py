"""
MicroPython program for Raspberry Pi Pico module
A 100ohm trim pot is between +3.3V and Ground.
Adjusting the pot changes the voltage fed to the Analog to Digital converter.
Micropython produces a 16 bit value of the voltage, which is then converted to 12 bit.

Reference:
https://github.com/micropython/micropython/blob/master/ports/rp2/machine_adc.c


Taylor series has been applied with adc.read_u16()
Range of 16 bit values is 0 to 65535
A bit-shift right of 4 reduces to 12 bit with a range of 0 to 4095

"""

from machine import ADC, Pin
import time
adc = ADC(Pin(26))
print(dir(adc))
print("adc.CORE_TEMP:",adc.CORE_TEMP) #4 channel number
print(dir(adc.__class__))
count = 0
bit16_previous = 0
while count < 50:
    bit16 = adc.read_u16() # Read 16 bit created number
    #bit16 = adc.read()    
    #print(type(bit16))
    bit12 = bit16 >> 4 # Convert to 12 bit with bit-shift right
    #print(adc.read_u16())
    if bit16 != bit16_previous:
        print(bit16, bit12)
    time.sleep(1)
    count += 1
    bit16_previous = bit16

"""   
Example output:
['__class__', 'CORE_TEMP', 'read_u16']
128 8
176 11
224 14
160 10
0 0
160 10
176 11
224 14
144 9
96 6
0 0
23957 1497
36184 2261
61967 3872
65535 4095
"""
