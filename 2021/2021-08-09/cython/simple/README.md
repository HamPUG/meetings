# simple cython example

Based on:

https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html

## Steps

* virtual env

  ```commandline
  virtualenv -p /usr/bin/python3 venv
  ./venv/bin/pip install cython
  ```

* create `helloworld.pyx`

  ```python
  print("hello world")
  ```

* create `setup.py`

  ```python
  from setuptools import setup
  from Cython.Build import cythonize
  
  setup(
      ext_modules = cythonize("helloworld.pyx")
  )
  ```

* compile

  ```commandline
  ./venv/bin/python setup.py build_ext --inplace
  ```

* use extension

  ```commandline
  ./venv/bin/python
  >>> import helloworld
  hello world
  ```

