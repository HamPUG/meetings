# timer_pin25_flash.py
# Demonstrate use of the Timer periodically run a callback that flashes the led
# on-board the Pico module via GPIO pin 25.

from machine import Pin, Timer
led = Pin(25, Pin.OUT)
tim = Timer()

def tick(timer):
    global led
    led.toggle()
    
tim.init(freq=2, mode=Timer.PERIODIC, callback=tick)
