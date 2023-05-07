# Countries-States-Cities

## Source

https://github.com/dr5hn/countries-states-cities-database/tree/master/csv

## Installation

```bash
./venv/bin/datasette install datasette-cluster-ma
```

## Import

```bash
csvs-to-sqlite data/csc-cities.csv -t cities data/countries-cities-states.db
csvs-to-sqlite data/csc-countries.csv -t countries data/countries-cities-states.db
csvs-to-sqlite data/csc-states.csv -t states data/countries-cities-states.db
```

