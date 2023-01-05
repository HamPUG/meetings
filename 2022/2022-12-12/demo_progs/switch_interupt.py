# switch_interupt.py
# Interupt driven switch
from machine import Pin
import time

# switch_1, when closed, connects GP14 (Pico 19) to the Ground rail.
# Pin.PULL_UP keeps the pin at 3.15V when swtich is open.
switch_1 = Pin(14, Pin.IN,  Pin.PULL_UP)
switch_1.irq(lambda pin: print("IRQ with flags:", pin.irq().flags()), Pin.IRQ_FALLING)

# Led on the Pico module, GP25.
led_1 = Pin(25, Pin.OUT)

while True:
    #print(dir(switch_1))
    print(switch_1.value()) # 1 when switch is off
    if switch_1.value() == 1:
        led_1.value(1)
    else:
        led_1.value(0)
    time.sleep(1)
 
