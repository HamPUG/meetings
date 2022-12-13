# pwm_pin25_dimmer.py
# Change the Pulse Width Modulation duty cycle from 0 to 65535 then back to 0

from machine import Pin, PWM
import time

pwm = PWM(Pin(25))
pwm.freq(1000)  # min = 8;  max = 125MHz = 125000000
#print(dir(pwm)) # ['__class__', 'deinit', 'duty_ns', 'duty_u16', 'freq']
print("Starting...")
start_time = time.time()

for i in range (65536):
    pwm.duty_u16(i)  # 0 to 65535
    time.sleep_us(20)
    
for i in reversed(range(65536)):
    pwm.duty_u16(i)  # 65535 to 0
    time.sleep_us(20)
    
print("...Ended")    
print("Duration: {} seconds".format(time.time() - start_time))    

