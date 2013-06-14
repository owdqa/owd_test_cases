#!/bin/bash
#
# Script to quickly change a test description.
#
TEST_NUM=${1:?"Syntax: $0 <test number> <new desc>"}
NEW_DESC=${2:?"Syntax: $0 <test number> <new desc>"}

TEST_FILE="test_${TEST_NUM}.py"
if [ ! -f "$TEST_FILE" ]
then
	printf "\nTest file \"$TEST_FILE\" could not be found (or isn't a regular file).\n\n"
	exit 1
fi

sed -e "s/^\(.*_Description *= *\"\)[^\"]*\(\".*$\)/\1$NEW_DESC\2/" $TEST_FILE > $TEST_FILE.new

if [ $? -eq 0 ]
then
	mv $TEST_FILE.new $TEST_FILE
	printf "\nChange *successful*. :)\n\n"
else
    printf "\nChange unsuccessful :(\n\n"
    exit 1
fi