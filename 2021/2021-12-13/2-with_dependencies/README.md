# With Dependencies

Outputs a numpy matrix with random values.

## Setup

```
virtualenv -p /usr/bin/python3 venv
./venv/bin/pip install -r requirements.txt
```

## Execution

```
./venv/bin/pyinstaller --hidden-import numpy --name with_dependencies runner.py
```

