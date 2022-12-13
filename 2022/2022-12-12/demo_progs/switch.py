# switch.py
# Simple switch that turns on/off the pin25 led.
# Not interupt driven. Updates every second.
#
import time
from machine import Pin

# switch_1 connects from pin14 to +3.3V rail.
switch_1 = Pin(14, Pin.IN,  Pin.PULL_DOWN)

led = Pin(25, Pin.OUT)

while True:
    #print(dir(switch_1))
    print("switch_1.value():", switch_1.value())  # 1 when switch is on
    if switch_1.value() == 1:
        led.value(1)
    else:
        led.value(0)
    time.sleep(1)
    
"""
>>> %Run -c $EDITOR_CONTENT

switch_1.value(): 0
switch_1.value(): 0
switch_1.value(): 0
switch_1.value(): 0
switch_1.value(): 1
switch_1.value(): 1
switch_1.value(): 0
switch_1.value(): 0
switch_1.value(): 1
switch_1.value(): 1
switch_1.value(): 0    
"""
