To get the tests going:
1. Download data for the `csv` format from: https://github.com/synthetichealth/synthea-sample-data
2. Export the zip file with the csv data into this directory. It should be a dir called `csv`

So your final file structure should be:
```
./synthea_csv-pydantic
├── LICENSE
├── README.md
├── pyproject.toml
├── synthea_pydantic
│   ├── __init__.py
│   ├── allergies.py
│   ├── ...
│   └── supplies.py
├── tests
│   ├── data
│   │   ├── README.txt
│   │   └── csv
│   │       ├── allergies.csv
│   │       ├── ...
│   │       └── supplies.csv
│   ├── __init__.py
│   ├── test_allergies.py
│   ├── ...
│   └── test_supplies.py
└── uv.lock
```