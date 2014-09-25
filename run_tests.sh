#!/bin/bash

# Set up the environment.
. $HOME/.OWD_TEST_TOOLKIT_LOCATION
export owd_test_cases_DIR=$PWD

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

python ./tests/device_config.py -c ./tests/devices.cfg
source ./.OWD_DEVICE_CONFIG

# Symbolic link to .config file for publishing apps in the fake OWD-store
if [ -f ~/.config_loop_to_market ]
then
    ln -s ~/.config_loop_to_market tests/LOOP/aux_files/loop-to-market/.config > /dev/null 2>/dev/null
else
    echo "################################################## WARNING ##################################################"
    echo "Looks like you do not have any config file for publishing apps (like LOOP) to our own market store."
    echo "Therefore, tests containing that feature (like LOOP) will surely crash."
    echo "This script will continue its execution, but you may want to have that file in its right place."
    echo "#############################################################################################################"
fi

# Make sure nothing else is running first.
$OWD_TEST_TOOLKIT_BIN/wait_for_no_other_test_run.sh $$

# Now run the tests.
$OWD_TEST_TOOLKIT_BIN/execute_tests.sh $@
