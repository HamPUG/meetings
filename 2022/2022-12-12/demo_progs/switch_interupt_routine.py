# switch_interupt_routine.py
# Two switches generate interupts and toggle the Pico module led GP25
# and an external led GP16 (Pico 21).
# Add a 40ms delay to try an overcome "switch bounce".
# Swtich_1 when closed connects GP14 (Pico 19) to Ground.
# Swtich_2 when closed connects GP15 (Pico 20) to +3V3 out (Pico 37)
from machine import Pin
import time
#print(dir(time))

switch_1 = Pin(14, Pin.IN,  Pin.PULL_UP)
switch_2 = Pin(15, Pin.IN,  Pin.PULL_DOWN)
led_1 = Pin(16, Pin.OUT)
led_2 = Pin(25, Pin.OUT)

def toggle_led():
    #print(switch_1.value())
    if switch_1.value() == 1:
        time.sleep_ms(40) # Time delay to reduce switch bounce impact
        if switch_1.value() == 1:
            led_1.toggle()
            led_2.toggle()
            
    if switch_2.value() == 1:
        time.sleep_ms(40) # Time delay to reduce switch bounce impact
        if switch_2.value() == 1:
            led_1.toggle()
            led_2.toggle()

# Set up interupt request for the switches          
switch_1.irq(lambda pin: toggle_led(), Pin.IRQ_FALLING)
switch_2.irq(lambda pin: toggle_led(), Pin.IRQ_RISING)

while True:
    # Waiting for a switch to be pushed and generate an interupt which will
    # call toggle_led() routine.
    time.sleep(1)

