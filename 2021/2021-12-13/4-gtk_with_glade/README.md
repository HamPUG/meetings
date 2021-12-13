# GTK

GTK user interface constructed from Glade-generated XML file.

## Setup

```
virtualenv -p /usr/bin/python3 venv
./venv/bin/pip install -r requirements.txt
```

## Execution

```
./venv/bin/pyinstaller --add-data glade_gui.glade:. glade_gui.py
```

