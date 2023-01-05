# switch.py
# Switch that turns on/off the GP25 led.
# Not interupt driven. Updates every second.

import time
from machine import Pin

# switch_1, when closed, connects pin14 to the ground rail.
# Pin.PULL_UP keeps the pin at 3.15V when swtich is open.
switch_1 = Pin(14, Pin.IN,  Pin.PULL_UP)

# Led on the Pico module, GP25.
led_1 = Pin(25, Pin.OUT)

while True:
    #print(dir(switch_1))
    print("switch_1.value():", switch_1.value())  # 1 when switch is off
    if switch_1.value() == 1:
        led_1.value(1)
    else:
        led_1.value(0)
    time.sleep(1)

