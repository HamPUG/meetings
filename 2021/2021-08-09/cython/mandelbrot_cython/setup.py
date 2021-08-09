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

