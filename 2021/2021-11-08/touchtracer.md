# Touchtracer

Commands used to install kivy on new install of Ubuntu Mate 20.04.3 and 
hightlights of the console log from executing the commands 

Summay of commands to install Kivy:

## Prerequisites

Install extra apps with apt...

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

Remain in Kivy Virtual envrionment from here onwards...

## Install Kivy and Kivy examples

```bash
python -m pip install kivy[base] kivy_examples
```

## Try out Touchtracer example

```bash
ls -l ~/kivy_venv/share/kivy-examples/demo/touchtracer/
python ~/kivy_venv/share/kivy-examples/demo/touchtracer/main.py
```

Make a local kivy folder and copy touchtracer to it and try it out...

```bash
mkdir kivy
cd kivy
# copy to kivy folder
cp -R ~/kivy_venv/share/kivy-examples/demo/touchtracer/ touchtracer/
ls -l touchtracer
cd touchtracer/
python main.py
```

## Install buildozer, which needs Cython

```bash
pip install Cython --install-option="--no-cython-compile"
pip install buildozer
```

Use buildozer to make an apk file of the Touchtracer application in /bin folder. 
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

## Deploy

Plug in the phone via USB cable, with USB debugging and File Transfer mode.

```bash
buildozer android deploy 
```

This will fail. A message on phone states:...

```
Allow USB debugging?

The computer RSA key fingerprint is:

FD: ... :BD

[] Always allow from this computer

Cancel Allow
```

Check and click Allow

Deploy a second time....

```bash
buildozer android deploy 
```

...This time the Touch tracer app is on the phone and appears in the phone menu.

Adding `scrcpy` (Screen Copy), allows a phone screen to be displayed as a window on
a PC. Connection can be via wifi or USB cable.

This github site provides the latest (V1.19) source code for scrcpy...

https://github.com/Genymobile/scrcpy

...however it is in the Ubuntu repository and not too many version behind, so
easier to install with apt.

```bash
(kivy_venv) ian@kivy:~/kivy/touchtracer$ apt search scrcpy
Sorting... Done
Full Text Search... Done
scrcpy/focal 1.12.1+ds-1 amd64
  Display and control your Android device

sudo apt install scrcpy
```

Adding the Kivy Launcher is done with GUI so its best to show this in an Impress
slide show.

Note: If everything gets screwed up, then try...

```bash
buildozer distclean
```

Do these later if required...

These installs may have just been for **showcase** example...

```bash
$ sudo apt install xclip xsel
```
