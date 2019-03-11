# Tensorflow on RPi3

Instructions and code are based on:

* https://github.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi
* https://raw.githubusercontent.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi/master/Object_detection_picamera.py

Base image is Raspbian Stretch lite 2018-11-13:

* https://www.raspberrypi.org/downloads/raspbian/
* http://director.downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13-raspbian-stretch-lite.zip

## Installation

install required dependencies:

* virtual environments

  ```
  sudo apt-get install virtualenv
  ```

* tensorflow

  ```
  sudo apt-get install git
  sudo apt-get install libatlas-base-dev
  sudo apt-get install python3-tk python3-dev
  sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
  sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
  sudo apt-get install libxvidcore-dev libx264-dev
  sudo apt-get install qt4-dev-tools
  sudo apt-get install protobuf-compiler
  sudo apt-get install libilmbase12
  sudo apt-get install libopenexr22
  sudo apt-get install ibgstreamer1.0-0
  ```

* create tensorflow dir:

  ```
  cd ~
  mkdir tf
  cd tf
  ```

* get tensorflow (https://github.com/lhelontra/tensorflow-on-arm/releases):

  ```
  wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.8.0/tensorflow-1.8.0-cp35-none-linux_armv7l.whl
  ```

* create virtualenv:

  ```
  virtualenv -p /usr/bin/python3.5 venv
  venv/bin/pip install tensorflow-1.8.0-cp35-none-linux_armv7l.whl
  venv/bin/pip install opencv-python
  venv/bin/pip install matplotlib
  venv/bin/pip install pillow
  ```

* clone tensorflow models:

  ```
  git clone --recurse-submodules https://github.com/tensorflow/models.git
  ```

* update PYTHONPATH (~/.bashrc):

  ```
  export PYTHONPATH=$PYTHONPATH:/home/pi/tf/models/research:/home/pi/tf/models/research/slim
  ```

* compile the protobufs:

  ```
  cd ~/tf/models/research
  protoc object_detection/protos/*.proto --python_out=.
  ```

* download SSD model from tensorflow model zoo:

  ```
  cd ~/tf/models/research/object_detection/
  wget http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
  tar -xzvf ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
  ```

* place `object_detection_webcam.py` in `~/tf/models/research/object_detection`

