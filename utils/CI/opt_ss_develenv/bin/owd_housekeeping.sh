#!/bin/bash
#
# Script to manage housekeeping for automated owd tests.
#
# NOTE: Deliberately uses hardcoded path names since we're
# removing directories and subfolders.
#
printf "\n\n"

echo "/tmp/tests"
echo "=========="
cd /tmp/tests 
if [ $? -eq 0 ]
then
	FOUND=""
	find -mtime +14 | while read dirnam
	do
		FOUND="Y"
		echo "Removing $dirnam ..."
		rm -rf $dirnam
	done

	[ ! "$FOUND" ] && echo "(nothing old enough to remove)"
else
	echo "Failed to reach this dir, so ignoring and moving on."
fi

printf "\n\n"

echo "/var/www/html/owd_tests"
echo "======================="
cd /var/www/html/owd_tests
if [ $? -eq 0 ]
then
	FOUND=""
	find -mtime +14 | while read dirnam
	do
		FOUND="Y"
		echo "Removing $dirnam ..."
		rm -rf $dirnam
	done

	[ ! "$FOUND" ] && echo "(nothing old enough to remove)"
else
	echo "Failed to reach this dir, so ignoring and moving on."
fi

printf "\n\n"
