# pin25_blink_toggle.py
# Blink led connected to pin 25 at 1 second intervals

import time
from machine import Pin
led = Pin(25, Pin.OUT) # Led on Pico module

print("Start blinking...")
for i in range(10):
    # Use toggle instead of value(1)/value(0), etc.
    led.toggle()
    time.sleep_ms(500)

print("...Stopped blinking.")

