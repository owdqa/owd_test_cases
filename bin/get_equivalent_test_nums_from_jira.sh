#!/bin/bash
#
# Gets a cross-reference of test numbers from JIRA test match the
# tests in test/ folder (based on _Description).
#
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

BRANCH=$1

# First, get the test numbers from JIRA into a temp file (with single spaces).
TMPFILE=$(${OWD_TEST_TOOLKIT_DIR}/../owd_test_cases/bin/get_test_list_from_jira.sh $BRANCH)
TESTDIR=${OWD_TEST_TOOLKIT_DIR}/../owd_test_cases/tests

if [ $? -ne 0 ]
then
	exit 1
fi

printf "\nJira test cases for branch \"${BRANCH:-"(unknown)"}\" vs. current tests:\n\n"
printf "%-7s    %-7s %s\n" "Jira" "Current" "Descripion"
printf "%-7s    %-7s   \n" "ID"   "ID"
printf "%0.1s" "="{1..80}
printf "\n"

# Now scan each of our tests and report the equivalent test numbers (removing 'clutter').
grep "_Description" $TESTDIR/test_*.py  | \
sed -e "s/tests\/test_//"               | \
sed -e "s/\.py: *_Description = \"/\t/" | \
sed -e "s/\[.*\]//g"                    | \
sed -e "s/(BLOCKED BY .*) *//g"         | \
sed -e "s/\*.*\*//g"                    | \
sed -e "s/CLONE *- *//"                 | \
sed -e "s/\t */\t/"                     | \
sed -e "s/\.*\"$//"                     | \
while read line
do
    CURR_TEST_NUM=$( echo "$line" | awk 'BEGIN{FS="\t"}{print $1}')
    CURR_TEST_DESC=$(echo "$line" | awk 'BEGIN{FS="\t"}{print $2}')
    
    grep -i -P "\t$CURR_TEST_DESC$" $TMPFILE | \
    awk '{FS="\t"}{print $1}'                | \
    while read TEST_NUM
    do 
    	printf "%-7s" $TEST_NUM
    	printf " => %-7s %s\n" $CURR_TEST_NUM "$CURR_TEST_DESC"
    done
done

printf "\n\n"   
