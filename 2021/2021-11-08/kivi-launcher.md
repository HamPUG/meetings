# kivi-launcher

Install [Kivy Launcher](https://github.com/kivy/kivy-launcher) from Github repository. 

Kivy_Launcher may be in the google play store, but it may be out-of-date and only support python2.

An up-to-date release can be obtained from github.

```bash
source ~/kivy_venv/bin/activate
cd kivy
```

Get kivi-launcher source code

```bash
wget https://github.com/kivy/kivy-launcher/archive/main.tar.gz
tar -xzf main.tar.gz -C ~/kivy/
cd kivy-launcher-main/
```

Edit `buildozer.spec` file:

```bash
pluma buildozer.spec
```

Make this change (since 2.0.0 is out)...

```ini
# Kivy version to use
#osx.kivy_version = 1.9.1
osx.kivy_version = 2.0.0
```

Note these default settings. It will use Python3 and build for a 32-bit ARM chip phone.

```ini
# change the major version of python used by the app
osx.python_version = 3

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86
android.arch = armeabi-v7a
```

Now use Buildozer to add the Kivy-launcher to the phone...
Takes about 10 minutes...

```bash
buildozer android debug
```

Now deploy to phone...

```bash
buildozer android deploy
```

Kivy Launcher is now on the phone menu.

Launch and get screen: "Allow Kivy Launcher to access photos, media and files on your device?"

Select *Allow*

```
Please install applications in one of the following directories
storage/emulated/0/kivy
```


OR:

* Wait a while and click on "reload" if files exist in `<internal shared storage>/kivy/`

* This time it finds files in `<internal shared storage>/kivy/`

* Goto GUI File Manager on your Linux machine. Andoid has `<internal shared storage>`

* Create a `kivy` folder

* `<internal shared storage>` contains folder `kivy`

* Drag and drop Touchtrace folder from `~/kivy/` to `Android/internal shared storage/kivy/`

* Kivy Launcher should now find Touchtrace.

* Double tap to launch Touchtrace

You may edit the main.py in the `Android/internal shared storage/kivy/touchtracer/` folder. Then get Kivy Launcher to re-launch Touchtracer. The changes made to the code may now be observed.


## Documentation

For documentation on programming in *Kivy* :

* https://kivy.org/doc/stable/
