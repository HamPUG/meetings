# Console scripts

Reutemann will briefly discuss how you can add "console scripts" to your
library (and how to reference them in the library's setup.py), to simplify
calling your scripts from the command-line.

## Installation

* create a virtual environment

  ```
  virtualenv -p /usr/bin/python3.7 venv
  ```

* install code (from within this directory)

  ```
  ./venv/bin/pip install .
  ```

## Testing

You can test the console script like this:

```
./venv/bin/msdp-hello
```


## Further information

* [setuptools](https://github.com/HamPUG/meetings/tree/master/2018/2018-02-12/setuptools_pypi_mkdocs)
