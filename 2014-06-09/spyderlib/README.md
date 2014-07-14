Spyder - first impressions
===

Download:
https://bitbucket.org/spyder-ide/spyderlib

(Note: It used to be on Google Code but has now migrated to Bitbucket.)

![spyderlib](https://raw.githubusercontent.com/HamPUG/meetings/master/2014-06-09/spyderlib/screenshot.png)

Upsides
---

* Easy on Ubuntu, `apt-get install spyder`. Yes you can also do `pip install spyder` but you'd need to handle all of the dependencies, like `PyQt4`, etc.

* Runs fast, doesn't feel particularly complicated.

* Has IPython support.

Downsides
---

* Was a pain to install on Windows - I believe the standalone .exe installer has dependencies you have to download. Otherwise you can get it with Python distributions like `Anaconda`.

* UI is not particularly splendid, unlike PyCharm!

* Can't seem to get a fully dark colour scheme going on with the UI (see the screenshot so you know what I mean).

* Debugging is not the same feel as Eclipse or Visual Studio, the debugging visualization is not within the editor window but within the interpreter window. So it's not particularly as intuitive.

Quirks
---

* On my laptop (which is Xubuntu), I had this weird issue where starting up Spyder (by typing in `spyder` on the terminal) did not end up opening the application. It didn't even show up in the list of processes. I had to basically type this instead: `spyder --new-instance`. I'm not sure as to why I have to do this, but I thought I'd let you know.
