#!/bin/bash
#
# Recreates the table of tests covered, to be inserted into the 
# README.md file for a test project.
#
THISDIR=$(dirname $0)
DESC_FILE=$THISDIR/../Docs/test_descriptions

#
# Start the table off.
#
echo "<!--testcoverage-->
TESTS COVERED
=============
<table>
  <tr>
    <th>Test Case</th><th>Description</th>
  </tr>"

#
# Create the rows.
#
find . -name "test_*.py" | while read fnam
do
	TEST_NAME=$(echo $fnam | sed -e "s/^.*\/test_\(.*\).py$/\1/")
    TEST_DESC=$(egrep "^$TEST_NAME\|" $DESC_FILE | awk 'BEGIN{FS="|"}{print $2}')

    echo "
  <tr>
    <td  align=center>$TEST_NAME</td><td  align=left>$TEST_DESC</td>
  </tr>"
done

#
# Finish the table off.
#
echo  "</table>"
