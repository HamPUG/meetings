# Pandas

*pandas* is an open source, BSD-licensed library providing high-performance,
easy-to-use data structures and data analysis tools for the Python
programming language.

http://pandas.pydata.org/

## Setup
```
sudo apt-get install libmysqlclient-dev
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

Number of dependencies:

```
$ ./venv/bin/pip freeze | wc -l
8
```

## What's happening

* converting SQLite employees database to MySQL
* extending table by inserting employee email address
* adding social media information (twitter handles) from a CSV file as separate table

## Pros/Cons

* P: very flexible
* C: loads all rows into memory (use chunking)
