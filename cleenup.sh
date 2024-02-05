#!/bin/bash

# Deletes all test data and last launch data, if exists.


echo
echo '----------------------------------------------------------------------------------------------------------'
echo "Cleaning last launch data!"
echo '----------------------------------------------------------------------------------------------------------'
echo

coverage_raw=.coverage
coverage_data=./htmlcov/
last_launch_results=weather_results.csv

if [ -f $coverage_raw ]; then
  (sudo rm -v $coverage_raw)
fi

if [ -d $coverage_data ]; then
  (sudo rm -rfv $coverage_data)
fi

if [ -f $last_launch_results ]; then
  (sudo rm -v $last_launch_results)
fi

echo
echo '----------------------------------------------------------------------------------------------------------'
echo "Finished cleaning!"
echo '----------------------------------------------------------------------------------------------------------'
echo
