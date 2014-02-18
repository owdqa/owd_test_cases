#!/bin/bash
#
# Prepare the dependencies for running OWD tests on the CI server.
#
DEVICE="$1"
BRANCH="$2"
TEST_TYPE="$3"

if [ ! "$DEVICE" ] || [ ! "$BRANCH" ] || [ ! "$TEST_TYPE" ]
then
	echo "Syntax: $0 <device> <branch> <test type>"
	exit 1
fi

[ ! "$HOME" ] && export HOME=/home/develenv
[ ! -d "$HOME/projects" ] && mkdir $HOME/projects

# Recursive delete with 'sudo', so be super paranoid here!
sudo rm -rf $HOME/projects/* 2>/dev/null

cd $HOME/projects
git clone https://github.com/owdqa/OWD_TEST_TOOLKIT.git >/tmp/${JOB_NAME}_${BUILD_NUMBER}.log 2>&1

#
# Now run the CI server setup script.
#
$HOME/projects/OWD_TEST_TOOLKIT/bin/ci_test_run.sh $DEVICE $BRANCH "$TEST_TYPE"
