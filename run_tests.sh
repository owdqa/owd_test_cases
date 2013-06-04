#!/bin/bash

# Set up the environment.
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

# Make sure nothing else is running first.
wait_for_no_other_test_run.sh $$

# Now run the tests.
run_all_tests.sh $@
