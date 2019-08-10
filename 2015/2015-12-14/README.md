# 2015-12-14
#### 21

## RPi.GPIO

Ian Stewart presented the RPi.GPIO python module.

The Raspberry Pi computer has a connector to provide physical access to connect
LED's and switches, etc., to the General Purpose Input and Output (GPIO)
signals. The python module RPi.GPIO allows a selection of pins on this
connector to be configured to receive input, or generate output signals.
RPi.GPIO also supports providing a Pulse Width Modulation (PWM) output signal.  

The Raspian distro provides a Debian based GUI desktop environment for the
Raspberry Pi. Included in Raspian are Python 2 & 3, the tkinter/ttk GUI tool
kit, and the Integrated Development Environment IDLE. Raspian also includes the
python module RPi.GPIO. 

As well as the slide show presentation material, there are 9 demonstration
programs to highlight features of the RPi.GPIO module. Most of these programs
utilize the tkinter GUI and use the themed tool kit (ttk). A brief summary of
these programs is as follows:

* 01_demo_get_pin.py – Display P1 Connector pins.
* 02_demo_rpi_package.py – Display information on the python Rpi.GPIO package.
* 03_demo_ttk_1_led.py – Using the tkinter GUI, turn on and off a LED.
* 04_demo_ttk_4_led_counter_simple.py – 4 x LED's counting in binary from 0 to 15.
* 05_demo_ttk_4_led_counter_complex.py - 4 x LED's counting in binary. Uses [::-1]
* 06_demo_ttk_4_led_counter_inc_dec.py – Use tkinker GUI to increment/decrement counter.
* 07_demo_ttk_2_switches.py – Receive input from two switches. NB: Run as sudo.
* 08_demo_ttk_pwm_linear.py – Pulse Width Modulation with a linear frequency scale.
* 09_demo_ttk_pwm_exponential.py - Pulse Width Modulation with an exponential scale.
