2022-12-12

# MicroPython on the Raspberry Pi Pico Module

**Ian Stewart** delivered a presentation introducing *MicroPython* on the *Raspberry Pi Pico* module.

The presentation is in two parts. 

* *Part 1* covers the hardware of the Raspberry Pi RP2040 chip and the Pico module.
* *Part 2* features installing MicroPython and using it to write code for the Pico module. 

The slide show presentations are in .ODP and .PDF formats:

* [ pico-presentation-part1.odp](pico-presentation-part1.odp)
* [ pico-presentation-part1.pdf](pico-presentation-part1.pdf)
* [ pico-presentation-part2.odp](pico-presentation-part2.odp)
* [ pico-presentation-part2.pdf](pico-presentation-part2.pdf) 

The following MicroPython programs were used for demonstration purposes:

* [adc_temp.py](demo_progs/adc_temp.py) Analog to Digital converter for RP2040 chip temperature, and voltage reading.
* [get_info.py](demo_progs/get_info.py) Display dir() and help().
* [pin16_blink.py](demo_progs/pin16_blink.py) Blink external led connected to pin16.
* [pin25_blink_toggle.py](demo_progs/pin25_blink_toggle.py) Use "toggle" method to blink Pico led.
* [pwm_pin25_dimmer.py](demo_progs/pwm_pin25_dimmer.py) Apply Pulse Width Modulation to Pico led to provide dimming of the led.
* [rtc_time.py](demo_progs/rtc_time.py) Display output from the Real Time Clock (RTC).
* [switch.py](demo_progs/switch.py) A simple switch.
* [switch_interupt.py](demo_progs/switch_interupt.py) Switch with Interupt Request.
* [switch_interupt_routine.py](demo_progs/switch_interupt_routine.py) Two switches with Interupt Request.
* [timer_pin25_flash.py](demo_progs/timer_pin25_flash.py) Use Timer to flash Pico led.
