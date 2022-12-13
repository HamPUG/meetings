# switch_interupt_routine.py
# Two switches can generate interupts and toggle the Pico led
# and an external led on pin 16.
# Add a 40ms delay to try an overcome "switch bounce".

from machine import Pin
import time
print(dir(time))

switch_1 = Pin(14, Pin.IN,  Pin.PULL_DOWN)
switch_2 = Pin(15, Pin.IN,  Pin.PULL_UP)
led = Pin(16, Pin.OUT)
led_2 = Pin(25, Pin.OUT)

def toggle_led():
    #print(switch_1.value())
    if switch_1.value() == 1:
        time.sleep_ms(40) # Time delay to reduce switch bounce impact
        if switch_1.value() == 1:
            led.toggle()
            led_2.toggle()
            
    if switch_2.value() == 1:
        time.sleep_ms(40) # Time delay to reduce switch bounce impact
        if switch_2.value() == 1:
            led.toggle()
            led_2.toggle()

# Set up interupt request            
switch_1.irq(lambda pin: toggle_led(), Pin.IRQ_RISING)
switch_2.irq(lambda pin: toggle_led(), Pin.IRQ_FALLING)

while True:
    # Waiting for a switch to be pushed and generate an interupt which will
    # call toggle_led() routine.
    time.sleep(1)

