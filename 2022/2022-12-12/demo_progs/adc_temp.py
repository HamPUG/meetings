# adc_temp.py
# There are 5 x Analog to Digital Converter channels.
# Sensitivity is 0 to 4096 which micropython multiplies by 16 for a range of
# 0 to 65536 in steps of 16
#
# Reading of 8177 is (8177-1)/16 = 511; 8161 is (8161-1)/16 = 510

# ADC(4) is an internal temperature sensor of the RP2040 chip.
# It does not come out on any GPIO pin.
# ADC(3) is GPIO29. This is a A to D conversion of a voltage.

import time
import machine

"""
# ADC 0 to 4
# 0 = GPIO26
# 1 = GPIO27
# 2 = GPIO28
# 3 ADC VREF (GPIO29) Voltage Sensor off Mosfet 3.3V. Measure of VSYS Voltage
    Via 200K/100K divider.

# 4 Internal to RP2040. Temperature Sensor

The temperature sensor measures the Vbe voltage of a biased bipolar diode,
connected to the fifth ADC channel.
Typically, the Vbe = 0.706V at 27 degrees C. 
        temp_sensor = machine.ADC(4)
        conversion_factor = 3.3 / 65535
        reading = temp_sensor.read_u16()
        reading = reading * conversion_factor
        temperature = 27 - (reading - 0.706) / 0.001721
        print("temperature:", temperature) 

Notes:
# GPIO23 PS0 PPM mode / PS1 PWM mode for 3.3V regulator
# GPIO24 5K6 / 10K of VBUS (from USB connector). RP2040. Ground 5K6 resistor?
# GPIO25 LED on RP2040
"""
voltage_sensor = machine.ADC(3)

temp_sensor = machine.ADC(4)
temp_conversion_factor = 3.3 / 65535

#  3.20 (ADC reading 8177) when VSYS is 4.83V
voltage_conversion_factor = 8177/4.83 # = 1693

def get_voltage():
    #voltage measured on GPIO29 = 3.20 when VSYS is 4.83V
    voltage = voltage_sensor.read_u16()    
    print("voltage reading:", voltage)
    voltage = voltage / voltage_conversion_factor
    print("voltage", "{:.2f}".format(voltage))
    # 8145, 8161, 8177 increments by 16 = 8177

def get_temp():
    reading = temp_sensor.read_u16()
    print("temp ADC reading:", reading) #reading 14275
    reading = reading * temp_conversion_factor
    print("temp_conversion:", reading) # 0.7188144

    temperature = 27 - (reading - 0.706) / 0.001721
    print("temperature: {:.2f}".format(temperature))     

while True:
    get_temp()
    get_voltage()
    time.sleep(2)
