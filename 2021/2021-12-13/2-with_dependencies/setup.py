from setuptools import setup


setup(
    name="pyinst-with-deps",
    description="PyInstaller test project with dependencies.",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
    ],
    packages=[
        "deps",
    ],
    install_requires=[
        "numpy",
    ],
    version="0.0.1",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    entry_points={
        "console_scripts": [
            "deps-run=deps.run:sys_main",
        ]
    }
)

