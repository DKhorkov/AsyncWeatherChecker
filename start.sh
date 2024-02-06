#!/bin/bash

# First of all, installs all requirements.
# Then, cleans project directory.
# After cleaning, runs test and collect coverage results.
# If all tests were successfully passed, than starts main app scrypt.


# Declaring constants.
# https://google.github.io/styleguide/shellguide.html#s7-naming-conventions
readonly BASH_ERROR_RETURN_CODE=1

sh configure.sh
sh cleenup.sh

# If not all tests were successfully passed and return code from run_tests.sh is equal to
# bash error return code, then exits and not launching main app.
# https://unix.stackexchange.com/questions/417499/bash-how-to-exit-from-secondary-script-and-from-the-main-script-on-both-time
sh run_tests.sh || exit $BASH_ERROR_RETURN_CODE

sh run_app.sh
