# python-console-scripts (complex dependencies)
Example repo for specifying console scripts in Python.

The example code uses
[docker-banner-gen](https://pypi.org/project/docker-banner-gen/) (manually
installed from a .deb package) to display text in the console but also has a
dependency for [numpy](https://pypi.org/project/numpy/) (available through the
distro's package management system).

In this example we show that the package managers aren't perfect and cannot
account for package that have been manually installed on the system that 
you are using for packaging.


## Testing

* set up a virtual environment

  ```
  virtualenv -p /usr/bin/python3.7 venv
  ```

* install the code (from within the directory of this README)

  ```
  ./venv/bin/pip install .
  ```

* and now you can run the [hello.py](src/msdp/hello.py) script using:

  ```
  ./venv/bin/msdp-hello --text "Hello World!"
  ```

* you can display the script's help using:

  ```
  ./venv/bin/msdp-hello --help
  ```

## Linux packaging

Before **packaging** ensure you have *docker-banner-gen* installed manually from this Debian package:

  https://github.com/waikato-datamining/docker-banner-gen/releases/download/v.0.0.6/python3-docker-banner-gen_0.0.6-1_all.deb

After **packaging** and before **testing** the package, uninstall *docker-banner-gen* again (basically simulating another machine which doesn't have this package installed):

```commandline
sudo dpkg -r python3-docker-banner-gen
```

### stdeb (Debian)

Using [stdeb](https://github.com/astraw/stdeb), you can build Debian packages 
(requires `python3-all` and `python3-stdeb` packages to be installed):

* clean up previous build

  ```commandline
  rm -f *.tar.gz && rm -Rf deb_dist
  ```

* build package

  ```commandline
  python3 setup.py --command-packages=stdeb.command bdist_deb
  ```
* print **information** on package:

  ```commandline
  dpkg -I deb_dist/python3-mysuperduperproject_0.0.1-1_all.deb
  ```
  
  should output something like this:
  
  ```commandline
   new Debian package, version 2.0.
   size 2952 bytes: control archive=1096 bytes.
       317 bytes,    10 lines      control              
       877 bytes,     9 lines      md5sums              
       179 bytes,     9 lines   *  postinst             #!/bin/sh
       429 bytes,    12 lines   *  prerm                #!/bin/sh
   Package: python3-mysuperduperproject
   Source: mysuperduperproject
   Version: 0.0.1-1
   Architecture: all
   Maintainer: Peter Reutemann <fracpete@gmail.com>
   Installed-Size: 21
   Depends: python3-docker-banner-gen, python3-numpy, python3:any (>= 3.3.2-2~)
   Section: python
   Priority: optional
   Description: My super duper Project.
  ```

  **Note:** The *python3-docker-banner-gen* got added as dependency even though
  this Python package is only available from pypi and not as Debian package.
  
* when simulating an **apt install** (after uninstalling *docker-banner-gen*) with:
  
  ```commandline
  gdebi --apt-line deb_dist/python3-mysuperduperproject_0.0.1-1_all.deb
  ```
  
  You get the following output (with unsatisfiable dependency *python3-docker-banner-gen*):
  
  ```commandline
  Reading package lists... Done
  Building dependency tree        
  Reading state information... Done
  Reading state information... Done
  This package is uninstallable
  Dependency is not satisfiable: python3-docker-banner-gen
  ```

  You will need to install the *docker-banner-gen* package manually.

### py2deb (Debian)

Using [py2deb](https://py2deb.readthedocs.io/en/latest/readme.html), you can
build Debian packages (you need to install the library with pip in your virtual
environment first).

* install py2deb

  ```commandline
  ./venv/bin/pip install py2deb
  ```

* clean up previous build

  ```commandline
  rm -f /tmp/*.deb
  ```

* build package (numpy dependency needs to be specified as system package, 
  otherwise you end up with an error message stating: *`setup.py bdist` 
  is not supported*)

  ```commandline
  ./venv/bin/py2deb --use-system-package=numpy,python3-numpy -r /tmp -- .
  ```
  
  **Note:** If your requirements are listed in `requirements.txt`, then use the
  following instead:
  
  ```commandline
  ./venv/bin/py2deb --use-system-package=numpy,python3-numpy -r /tmp -- -r requirements.txt
  ```

* print information on package:

  ```commandline
  dpkg -I /tmp/python3-mysuperduperproject_0.0.1_all.deb
  ```
  
  should output something like this:
  
  ```commandline
   new Debian package, version 2.0.
   size 6096 bytes: control archive=4092 bytes.
       332 bytes,     9 lines      control              
     15044 bytes,   397 lines   *  postinst             #!/usr/bin/python3.7
     15014 bytes,   397 lines   *  prerm                #!/usr/bin/python3.7
   Package: python3-mysuperduperproject
   Version: 0.0.1
   Maintainer: Peter Reutemann <fracpete@gmail.com>
   Description: Python package mysuperduperproject converted by py2deb on November 8, 2020 at 13:35
   Architecture: all
   Depends: python3-docker-banner-gen, python3-numpy, python3.7
   Priority: optional
   Section: python
   Installed-Size: 116
  ```

  **Note:** Uses the Python version of the virtual environment that py2deb belongs to
  as dependency. The *docker-banner-gen* is automatically assumed to be available
  as package *python3-docker-banner-gen*. 
  
* when simulating an **apt install** (after uninstalling *docker-banner-gen*) with:
  
  ```commandline
  gdebi --apt-line /tmp/python3-mysuperduperproject_0.0.1_all.deb
  ```
  
  You get the following output (with unsatisfiable dependency *python3-docker-banner-gen*):
  
  ```commandline
  Reading package lists... Done
  Building dependency tree        
  Reading state information... Done
  Reading state information... Done
  This package is uninstallable
  Dependency is not satisfiable: python3-docker-banner-gen
  ```

  You will need to install the *docker-banner-gen* package manually.

  
### fpm

[fpm](https://github.com/jordansissel/fpm) (effing package management; 
[documentation](https://fpm.readthedocs.io/en/latest/)) allows package generation 
for multiple platforms.

* install the tool

  ```commandline
  sudo apt-get install ruby ruby-dev rubygems build-essential
  sudo gem install --no-document fpm
  ```  

#### Debian
  
* clean up previous build

  ```commandline
  rm -f python3-mysuperduperproject*
  ```
  
* build package (use `--python-pip` to avoid error message `Need executable 'easy_install' to convert python to deb`)

  ```commandline
  fpm -s python -t deb --python-pip /usr/bin/pip3 --python-package-name-prefix python3 .
  ```
  
* print information on package:

  ```commandline
  dpkg -I python3-mysuperduperproject_0.0.1_all.deb
  ```
  
  should output something like this:
  
  ```commandline
   new Debian package, version 2.0.
   size 3456 bytes: control archive=816 bytes.
       289 bytes,    12 lines      control              
      1228 bytes,    12 lines      md5sums              
   Package: python3-mysuperduperproject
   Version: 0.0.1
   License: MIT License
   Vendor: none
   Architecture: all
   Maintainer: <fracpete@metal>
   Installed-Size: 3
   Depends: python3-numpy, python3-docker-banner-gen
   Section: default
   Priority: extra
   Homepage: UNKNOWN
   Description: My super duper Project.
  ```

  **Note:** The *docker-banner-gen* is automatically assumed to be available
  as package *python3-docker-banner-gen*. 
  
* when simulating an **apt install** (after uninstalling *docker-banner-gen*) with:
  
  ```commandline
  gdebi --apt-line python3-mysuperduperproject_0.0.1_all.deb
  ```
  
  You get the following output (with unsatisfiable dependency *python3-docker-banner-gen*):
  
  ```commandline
  Reading package lists... Done
  Building dependency tree        
  Reading state information... Done
  Reading state information... Done
  This package is uninstallable
  Dependency is not satisfiable: python3-docker-banner-gen
  ```

  You will need to install the *docker-banner-gen* package manually.

#### RPM
  
* clean up previous build

  ```commandline
  rm -f python3-mysuperduperproject*
  ```
  
* build package

  ```commandline
  fpm -s python -t rpm --python-pip /usr/bin/pip3 --python-package-name-prefix python3 .
  ```

* print information on package:

  ```commandline
  rpm -qpiR python3-mysuperduperproject-0.0.1-1.noarch.rpm
  ```
  
  should output something like this:
  
  ```commandline
  Name        : python3-mysuperduperproject
  Version     : 0.0.1
  Release     : 1
  Architecture: noarch
  Install Date: (not installed)
  Group       : default
  Size        : 3720
  License     : MIT License
  Signature   : (none)
  Source RPM  : python3-mysuperduperproject-0.0.1-1.src.rpm
  Build Date  : Sun 08 Nov 2020 16:33:27 NZDT
  Build Host  : metal
  Relocations : / 
  Packager    : <fracpete@metal>
  Vendor      : none
  URL         : UNKNOWN
  Summary     : My super duper Project.
  Description :
  My super duper Project.
  python3-docker-banner-gen
  python3-numpy
  rpmlib(CompressedFileNames) <= 3.0.4-1
  rpmlib(PayloadFilesHavePrefix) <= 4.0-1
  ```

  **Note:** The *docker-banner-gen* is automatically assumed to be available
  as package *python3-docker-banner-gen*. 
  
