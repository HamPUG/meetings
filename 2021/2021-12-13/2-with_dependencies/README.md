# With Dependencies

Outputs a numpy matrix with random values.

## Setup

```
virtualenv -p /usr/bin/python3 venv
./venv/bin/pip install -r requirements.txt
```

## Execution

In theory, it should find the numpy dependency:

```
./venv/bin/pyinstaller --name with_dependencies runner.py
```

But if it doesn't, then add it as `--hidden-import`:

```
./venv/bin/pyinstaller --hidden-import numpy --name with_dependencies runner.py
```

