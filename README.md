# SmallCartography

## Install dependencies
- '$ bash install.sh`

## Running the master
- `$ python run.py --host=[host of the master] --port=[port of the master] --program=master`

## Running a mapper
- `$ python run.py --host=[host of the mapper] --port=[port of the mapper] --program=mapper\
        --ns_host=[host of the master] --ns_port=[port of the master] --name=[name of the mapper]`

## Running a reducer
- `$ python run.py --host=[host of the reducer] --port=[port of the reducer] --program=reducer\
        --ns_host=[host of the master] --ns_port=[port of the master] --name=[name of the reducer]`

## Running the test client for word counting
- This will count the frequencies of words of Hamlet using MapReduce
- `$ python tests/count_test.py`
