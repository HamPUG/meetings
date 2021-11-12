# 2021-11-08

Peter Reutemann's hands-on presentation highlights features of:

* [kivy](https://kivy.org/), a free and open source Python framework for developing mobile apps and other multitouch application software with a natural user interface (NUI). 

* [buildozer](https://buildozer.io/), providing build automation and deployment for iOS, Android and OSX developers. 

* [kivy launcher](https://github.com/kivy/kivy-launcher), an Android application that runs any Kivy examples stored on your mobile phones SD Card. It avoids having to compile your kivy projects to an APK.


At the NZPUG-Hamilton meeting on [9th March 2020](https://github.com/HamPUG/meetings/tree/master/2020/2020-03-09/ian), Ian Stewart delivered a presentation on the Kivy and Buildozer applications.

With a Ubuntu-Mate 19.10 PC platform he used APT to install python3-kivy V1.10.1 and Pip to install Buildozer V1.0. The applications that ran on the mobile phone were Python 2.


The current release of Kivy is V2.0.0 and Buildozer is V1.2. Using these releases, applicatons that are built and deployed to the mobile phone run Python 3.

There is also a package called *Kivy Launcher* that allows on-the-fly testing and modification of code that is being developed.

In this presentation Peter provides a hands on session with the latest versions of Kivy and Buildozer applications and introduces Kivy Launcher.

The presentation material is in two parts:

* [Touch tracer](touchtracer.md) highlights the steps involved in installation and operation of Kivy and Buildozer. The Kivy Examples application, *Touch tracer* is used to demonstate testing on a PC, building an APK, deploying the APK to a phone, and running the application on a phone.

* [kivi launcher](kivi-launcher.md) is built as an APK and deployed to the phone. The source code of *Touch Tracer* application is copied to the phones SD Card. Kivy Launcher then runs *Touch Tracer*. Changes to the source code may be performed by directly editing the Python files on the phones SD Card.

Peter's presentation was recorded and may be viewed at:

https://bbb.nzoss.nz/playback/presentation/2.0/playback.html?meetingId=6edc548c22debac4fb66721972cc80a03ddb3f87-1636351033522
