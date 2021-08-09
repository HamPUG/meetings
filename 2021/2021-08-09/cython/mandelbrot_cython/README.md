# Mandelbrot set (Cython)

## Setup

Set up virtual environment:

```commandline
virtualenv -p /usr/bin/python3 venv
./venv/bin/pip install numpy pillow colour cython
```

Configure `setup.py` to compile module:

```python
from setuptools import setup
from Cython.Build import cythonize

setup(
    install_requires=[
        "numpy",
        "pillow",
        "colour",
        "cython",
    ],
    ext_modules = cythonize("mandelbrot.pyx")
)
```

**NB:** When installing the library with `pip` via this `setup.py`
then `cython` must be installed manually beforehand (otherwise, the
import from Cython will fail).

## Compilation

```commandline
./venv/bin/python setup.py build_ext --inplace
```

## Execution

```commandline
./venv/bin/python -c "import mandelbrot"
```

