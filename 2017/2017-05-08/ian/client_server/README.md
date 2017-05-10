## Client Server Presentation

Although it might not be obvious, this presentation is about making a speedometer for a bicycle. This speedometer configuration is more conceptual than practical, as it would be rather difficult to ride a bike while looking at a monitor and using a keyboard and mouse. It is designed to introduce you to the client / server programming methodology and the python libraries pydbus, RPi.GPIO, and GTK+.

From the hardware perspective it involves:
* A bicycle with a magnet attached to the spokes.[1]
* A hall effect sensor chip to detect rotation of the bike wheel.[1]
* A Raspberry Pi ARM architecture computer.[1]
* A GUI display screen, keyboard and mouse.

[1]: Testing with simulated input may be performed on a i386 / AMD64 Linux desktop or laptop computer. Running these applications on a laptop may help with understanding client / server methodology.

From the sofware perspective it utilizes:
* RPi.GPIO python library to provide a call_back to count every rotation of the wheel.
* A repeating timer class to provide a call_back at a fixed interval of, say, one second.
* Utilizing the real time clock with the built-in time.time() to have time in days, hours, minutes and seconds.
* A server application to capture the wheel rotations and perform speed calculations.
* A client application to provide the GUI.
* Uses the pydbus library to provide DBus interprocess communications between the client and the server applications. Pydbus is a python wrapper for the DBus components of the GObject Introspection repository.


### Installation

* If using a Raspberry Pi then install the Raspbian distro or the Ubuntu Mate distro for the R-Pi 2 or 3. If simulating on a desktop/laptop then use a linux distro. E.g. Ubuntu.

* Both Raspbian and Ubuntu Mate (for R-Pi) include the RPi.GPIO python module for interacting with the R-Pi's GPIO pins.

* If you have a Raspberry Pi and a Hall Effect sensor module. Connect the Hall Effect sensor to, say, GPIO channel number 2 on the Raspberry Pi.

* The pydbus library is unlike to have been included with your Raspbian/Ubuntu distro. Enter this console command to install it from the PyPI repository. $ pip3 install pydbus

* From this github folder copy these gtk_client.py and server.py to your computer.

* Open one console terminal window, set default to the folder with these client and server applications, and type $ python3 server.py

* Open another console terminal window, set default to the folder with these client and server applications and type $ python3 gtk_client.py

* The GUI should now open and if you start riding your bike then you should be getting distances and speeds being displayed. Edit the source code on server.py to set your wheel_circumference to the correct number of meters.

* If you don't have a R-Pi or hall-effect sensor, then you should see speeds and distances changing on the GUI display as a result of random numbers being generated to simulate wheel rotations.


### Future

While this demonstrates the client / server methodology, enhancements to this code in the future may be: 

* Have one GUI but have multiple server processes supplying data from a variety of sources.

* Have servers that "emit" their data over the DBus, rather than supplying it on commands received from the client.


### Contents
* client_server_presentation.odp - Presentation slide show for Impress, etc.
* gtk_client.py
* server.py
* README.md - This file.

### Presentation

Presented at Hamilton Python User Group meeting on Monday, 8 May 2017, by Ian Stewart.


