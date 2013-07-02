#!/bin/bash
#
# Refreshes the test coverage table in the README.md file in the current directory.
#
CURRDIR=$(pwd)
THISDIR=$(dirname $0)

$THISDIR/refresh_test_descriptions.sh Y

cat ./README.md | while read line
do
	x=$(echo $line | grep "<!--testcoverage-->")
	if [ "$x" ]
	then
		break
	else
	   echo "$line"
	fi
done > ./README.new

$THISDIR/create_tests_covered_table.sh >> ./README.new

mv ./README.new ./README.md
