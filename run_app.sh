#!/bin/bash

# Runs Asynchronous Weather Checker.

readonly APP_SUCCESS_RETURN_CODE=0

echo
echo '----------------------------------------------------------------------------------------------------------'
echo "Launching Asynchronous Weather Checker!"
echo '----------------------------------------------------------------------------------------------------------'
echo

python3 src/main.py
readonly APP_RETURN_CODE=$?

if [ $APP_RETURN_CODE != $APP_SUCCESS_RETURN_CODE ]; then
  echo "Some problems appeared with Asynchronous Weather Checker! Please, check logs."
fi

echo
echo '----------------------------------------------------------------------------------------------------------'
echo "Asynchronous Weather Checker finished working!"
echo '----------------------------------------------------------------------------------------------------------'
echo
