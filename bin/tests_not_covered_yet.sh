#!/bin/bash
#
# Quick script to show me which tests are outstanding (uses a list from Jira and compares it to the tests we have).
#
. ~/.OWD_TEST_TOOLKIT_LOCATION

cd $OWD_TEST_TOOLKIT_DIR/../owd_test_cases/tests

#
# Match on desc, in case we're using a different test number.
#
cat ../Docs/tests.txt | while read line
do
    num=$( echo "$line" | awk '{FS="\t"}{print $1}' | awk 'BEGIN{FS="-"}{print $NF}')
    desc=$(echo "$line" | awk 'BEGIN{FS="\t"}{print $NF}' | sed -e "s/(/\\\(/g" | sed -e "s/)/\\\)/g")

    x=$(egrep -l "_Description *.*\]* *$desc\.*\"$" test_*.py)

    [ ! "$x" ] && printf "$num\t$desc\n"
done | while read line2
do
    #
    # Sometimes the description isn't fully correct, so this is the 2nd way of making sure ...
    #
    num=$( echo "$line2" | awk '{FS="\t"}{print $1}')
    desc=$(echo "$line2" | awk 'BEGIN{FS="\t"}{print $2}')

    [ ! -f test_${num}.py ] && echo "$num: $desc"
done
