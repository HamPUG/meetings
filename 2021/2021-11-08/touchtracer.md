# Touchtracer

This guide provides the commands used to install *Kivy* and *Buildozer* on a new installation of Ubuntu Mate 20.04.3 which has been brought up-to-date with the latest patches.


Summary of commands to install Kivy:

## Prerequisites

Use Advanced Package Tool, *apt*, to install prerequisite applications of *Kivy* and *Buildozer*...

```bash
sudo apt install python-is-python3 python3-pip git openjdk-8-jdk
sudo apt install libssl-dev automake autoconf libltdl-dev lld libffi-dev
```

## Build the virtual environment

```bash
python -m pip install --upgrade pip testresources setuptools virtualenv 
python -m virtualenv kivy_venv
source kivy_venv/bin/activate
```

NOTE: Remain in Kivy Virtual envrionment from here onwards...

## Install Kivy and Kivy examples

```bash
python -m pip install kivy[base] kivy_examples
```

## Try out the Touchtracer example

```bash
ls -l ~/kivy_venv/share/kivy-examples/demo/touchtracer/
python ~/kivy_venv/share/kivy-examples/demo/touchtracer/main.py
```

A window opens on the PC running the *Touch tracer* application. Mouse buttons are used to simulate the multi-touch control that would be used if the application was running on a phone. 

## Try out the Touchtracer example in a local folder.

Make a local kivy folder and copy touchtracer to it and try it out...

```bash
mkdir kivy
cd kivy
cp -R ~/kivy_venv/share/kivy-examples/demo/touchtracer/ touchtracer/
ls -l touchtracer
cd touchtracer/
python main.py
```

Again a window opens on the PC running the *Touch tracer* application. The *Touch tracer* in this local kivy folder will now be built into an Android Package (APK) file. 

## Install buildozer, which needs Cython

```bash
pip install Cython --install-option="--no-cython-compile"
pip install buildozer
```

Use buildozer to make an APK file of the Touchtracer application in /bin folder. 
It will later be downloaded into the phone. Start with init to make the buildozer.spec file

```bash
buildozer init
```

Edit the `buildozer.spec` file...

```bash
pluma buildozer.spec
```

And change the following lines:

```ini
# (str) Title of your application
#title = My Application
title = Touch Tracer

# (str) Package name
#package.name = myapp
package.name = touchtracer

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
#orientation = portrait
orientation = all
```

Build the application - takes about 30 mins the first time.

```bash
buildozer android debug 
```

Upon completion a bin folder has been created contianing the file:

```bash
~/kivy/touchtracer/bin/touchtracer-0.1-armeabi-v7a-debug.apk 
```

This APK file needs to be deployed to the mobile phone. 


## Deployment to Mobile Phone

Plug in the phone via USB cable, with USB Debugging and File Transfer mode enabled.

```bash
buildozer android deploy 
```

This will fail the first time. A message on phone states:...

```
=========================================
=                                       =
= Allow USB debugging?                  =
=                                       =
= The computer RSA key fingerprint is:  =
=                                       =
= FD:... ...:BD                         =
=                                       =
= [] Always allow from this computer    =
=                                       =
= Cancel Allow                          =
=                                       =
=========================================
```

Check and click Allow

Deploy a second time....

```bash
buildozer android deploy 
```

...This time the Touch tracer app is installed on the phone and appears in the phone menu.



## Adding Scrcpy

Adding `scrcpy` (Screen Copy), allows a phone screen to be displayed as a window on
a PC. Connection can be via wifi or USB cable.

This github site provides the latest (V1.19) source code for scrcpy...

https://github.com/Genymobile/scrcpy

...however it is in the Ubuntu repository and not too many versions behind, so
easier to install with apt.

```bash
apt search scrcpy
Sorting... Done
Full Text Search... Done
scrcpy/focal 1.12.1+ds-1 amd64
  Display and control your Android device

sudo apt install scrcpy
```

With the phone connected to the PC by USB cable, run scrcpy:

```bash
scrcpy -m 1024
```


## Kivy Launcher

The second part of this presentation is the installation and operation of the [kivi launcher](kivi-launcher.md) 

