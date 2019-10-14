# 2019-10-14
#### 64

## Jupyter Widgets

Jupyter Notebook comes with lots of batteries included,
ie lots of widgets to make notebooks interactive.

Material kindly prepared and provided by Ian Stewart,
presented by Peter Reutemann.

### Repositories

You can access all the example notebooks demonstrating the widgets
from these Github repositories:

* https://github.com/irsbugs/jupyter-notebook-widgets
* https://github.com/irsbugs/asyncio_progress_bars
* https://github.com/irsbugs/widgets-ubuntu-versions

### Setup

* create virtual environment

  ```
  virtualenv -p /usr/bin/python3.7 venv
  ```

* install jupyter

  ```
  ./venv/bin/pip install jupyter
  ```

* clone the repos into that directory:

  ```
  git clone https://github.com/irsbugs/jupyter-notebook-widgets.git
  git clone https://github.com/irsbugs/asyncio_progress_bars.git
  git clone https://github.com/irsbugs/widgets-ubuntu-versions.git
  ```

### Run

Start up Jupyter from within this directory:

```
./venv/bin/jupyter-notebook
```

