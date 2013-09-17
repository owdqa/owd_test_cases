#!/bin/bash

# Set up the environment.
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

if [ $? -ne 0 ] || [ ! -d $GAIATEST_PATH ]
then
	echo "
	** ERROR **
	
	It looks like OWD_TEST_TOOLKIT hasn't been installed correctly.
	Please clone OWD_TEST_TOOLKIT from github.com/owdqa and run \"./install.sh\",
	then retry this test.

"
	exit 1
fi

# Make sure nothing else is running first.
$OWD_TEST_TOOLKIT_BIN/wait_for_no_other_test_run.sh $$

# Now run the tests.
$OWD_TEST_TOOLKIT_BIN/execute_tests.sh $@
