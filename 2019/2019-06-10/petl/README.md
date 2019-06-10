# petl

**petl** is a general purpose Python package for extracting, transforming and
loading tables of data.

NB: Automatic table creation via SQLAlchemy.

## Setup

```
sudo apt-get install libmysqlclient-dev
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

## What's happening

* converting SQLite employees database to MySQL
* (almost) extending table by inserting employee email address
* adding social media information (twitter handles) from a CSV file as separate table

## Pros/Cons

* P: good documentation, lots of examples
* P: fast
* P: lots of utility functions
* C: extending table read from database/CSV cannot change their structure?

