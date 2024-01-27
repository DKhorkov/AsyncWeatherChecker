#!/bin/bash

# Runs test and collect coverage results.
# If not all tests were successfully passed, exits.
#
# Guide, how to catch pytest return code, provided below:
# https://copyprogramming.com/howto/get-pytest-exit-code-from-shell-script


readonly BASH_ERROR_RETURN_CODE=1

echo
echo '----------------------------------------------------------------------------------------------------------'
echo "Running all tests to check application correct work!"
echo '----------------------------------------------------------------------------------------------------------'
echo

readonly PYTEST_SUCCESS_RETURN_CODE=0

coverage run -m pytest -q
readonly PYTEST_RETURN_CODE=$?

if [ $PYTEST_RETURN_CODE != $PYTEST_SUCCESS_RETURN_CODE ]; then
  echo
  echo '----------------------------------------------------------------------------------------------------------'
  echo "Not starting Application due to the fact, that not all tests were successfully passed!"
  echo '----------------------------------------------------------------------------------------------------------'
  echo
  exit "$BASH_ERROR_RETURN_CODE"
fi

coverage html

echo
echo '----------------------------------------------------------------------------------------------------------'
echo "All tests were successfully passed!"
echo '----------------------------------------------------------------------------------------------------------'
echo
