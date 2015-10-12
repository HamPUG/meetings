begins
======

[begins](https://pypi.python.org/pypi/begins) is described as *Command line programs for busy developers*.
And you couldn't describe it any better. 

Example
-------
The following code can be invoked from the command-line and uses only two `begins` related lines:
```python
import begin
@begin.start
def run(name='Arther', quest='Holy Grail', colour='blue', *knights):
    "tis but a scratch!"
```

Generates the following beautiful command-line help:
```bash
usage: example.py [-h] [-n NAME] [-q QUEST] [-c COLOUR]
                  [knights [knights ...]]

tis but a scratch!

positional arguments:
  knights

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  (default: Arther)
  -q QUEST, --quest QUEST
                        (default: Holy Grail)
  -c COLOUR, --colour COLOUR
                        (default: blue)
```

Code
----

* `oldfashioned.py` -- using manually parsing of `sys.argv`
* `begins.py` -- same as `oldfashioned.py` but using `begins`
* `begins_additional.py` -- collects additional parameters
* `begins_mult.py` -- shows what happens when several method parameters start with the same character

