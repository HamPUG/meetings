# switch_interupt.py
# Interupt driven switch
from machine import Pin
import time

switch_1 = Pin(14, Pin.IN,  Pin.PULL_DOWN)
switch_1.irq(lambda pin: print("IRQ with flags:", pin.irq().flags()), Pin.IRQ_RISING)

led = Pin(25, Pin.OUT)

while True:
    #print(dir(switch_1))
    print(switch_1.value()) # 1 when switch is on
    if switch_1.value() == 1:
        led.value(1)
    else:
        led.value(0)
    time.sleep(1)
 
