Instructions to get the tests going:
1. Download data for the `csv` format from: https://github.com/synthetichealth/synthea-sample-data
2. Export the zip file with the csv data into this directory. It should be a dir called `csv`
  - So your final file structure should be:
```
synthea-pydantic/
  ...
  tests/
    data/
      csv/
        allergies.csv
        careplans.csv
        ... etc.
    test_allergies.py
    test_careplans.py
    ... etc
```