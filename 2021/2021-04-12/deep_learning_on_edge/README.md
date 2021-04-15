# Object Detection on Jetson Nano

## Install JetPack

For this example, 4.5 was used:

https://developer.nvidia.com/embedded/jetpack-archive

Custom PyTorch builds:

https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-8-0-now-available/72048
https://www.elinux.org/Jetson_Zoo#PyTorch_.28Caffe2.29

PyTorch docker images:

https://ngc.nvidia.com/catalog/containers/nvidia:l4t-pytorch


## Install necessary libraries

```commandline
sudo apt-get install python3-tk python3-dev libpython3-dev libopenblas-base libopenmpi-dev
```

## Pytorch

### Setup virtual environment

``` commandline
python3 -m venv venv
./venv/bin/pip install --upgrade pip setuptools
./venv/bin/pip install cython
./venv/bin/pip install "numpy<1.19.5"
./venv/bin/pip install torch==1.8.0
./venv/bin/pip install torchvision==0.9.1
./venv/bin/pip install opencv-python
./venv/bin/pip install matplotlib
```

### Example run

* Download images

  ```commandline
  wget https://www.wsha.org/wp-content/uploads/banner-diverse-group-of-people-2.jpg -O people.jpg
  wget https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/10best-cars-group-cropped-1542126037.jpg -O car.jpg
  wget https://cdn.pixabay.com/photo/2013/07/05/01/08/traffic-143391_960_720.jpg -O traffic.jpg
  wget https://images.unsplash.com/photo-1458169495136-854e4c39548a -O girl_cars.jpg
  ```

* Run code

  ```commandline
  ./venv/bin/python predict_image.py ./people.jpg
  ```

## TensorRT

* Follow instructions here:

  https://github.com/dusty-nv/jetson-inference/

* Once installed, you can make an inference like this:

  ```commandline
  detectnet --network=ssd-mobilenet-v2 images/peds_0.jpg images/test/output.jpg
  ```
 
