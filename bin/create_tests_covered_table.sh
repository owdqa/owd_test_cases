#!/bin/bash
#
# Recreates the table of tests covered, to be inserted into the 
# README.md file for a test project.
#
echo "<!--testcoverage-->
TESTS COVERED
=============
<table>
  <tr>
    <th>Test Case</th><th>Description</th>
  </tr>"
  
ls tests/test_*.py | while read fnam
do
	TEST_NAME=$(echo $fnam | sed -e "s/^.*\/test_\(.*\).py$/\1/")
	TEST_DESC=$(grep -i "_Description" $fnam | sed -e "s/^.*= *\"\([^\"]*\)\".*/\1/")

    echo "
  <tr>
    <td  align=center>$TEST_NAME</td><td  align=left>$TEST_DESC</td>
  </tr>"
done

echo  "</table>"