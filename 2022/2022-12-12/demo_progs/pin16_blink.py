# pin16_blink.py
# Blink led connected to pin 16 at 1 second intervals
import usys
import time
from machine import Pin
led = Pin(16, Pin.OUT)

print("Start blinking...")
for i in range(10):
    # .value(1) = .on()
    #led.value(1)
    led.on()
    time.sleep(1)
    #led.value(0)
    led.off()
    time.sleep(1)

print("...Stopped blinking.")
usys.exit()
