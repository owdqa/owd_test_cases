#!/bin/bash
#
echo "
Changes the test number in the filename and class name
for each test (saves them to a temporary folder for you
to check them before switching over).

Press ENTER to continue (or CTLR+c to quit).
"
read ans

#
# Set up dependencies.
#
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

#
# Loop through each test, presening the description and asking for the new number
#
TESTDIR=${OWD_TEST_TOOLKIT_DIR}/../owd_test_cases/tests
NEW_TESTDIR=/tmp/tests.new_$(date "+%H%M%S")
[ ! -d "$NEW_TESTDIR" ] && mkdir $NEW_TESTDIR

printf "\n*** CHANGED TESTS WILL BE SAVED TO $NEW_TESTDIR. ***\n\n"

declare -a test_arr
counter=0
while read fnam
do
	DESC=$(grep "_Description" $fnam | sed -e "s/^[^=]* *= *\"\([^\"]*\)\"/\1/")
	NUM=$( basename $fnam | awk 'BEGIN{FS="_"}{print $2}' | awk 'BEGIN{FS="."}{print $1}')
	
	test_arr[$counter]=$(printf "$NUM\t$DESC")
	counter=$((counter+1))
done <<EOF
$(ls $TESTDIR/test_*.py)
EOF

for i in "${test_arr[@]}"
do
    NUM=$( echo "$i" | awk 'BEGIN{FS="\t"}{print $1}')
    DESC=$(echo "$i" | awk 'BEGIN{FS="\t"}{print $2}')
    
    printf "\n-------------\n\n"
    printf "Current num : $NUM\n"
    printf "Current desc: $DESC\n\n"
    printf "New number  : "
    read new_num
    printf "New desc    : "
    read new_desc
    
    OLD_TEST=$TESTDIR/test_${NUM}.py
    NEW_TEST=$NEW_TESTDIR/test_${new_num}.py
    
    #
    # Do the change.
    #
    sed -e "s/^\([ \t]*class *test_\)[^(]*\((GaiaTestCase):\)/\1$new_num\2/" $OLD_TEST > ${NEW_TEST}.tmp
    sed -e "s/^\([ \t]*_Description *= *\"\)[^\"]*\(\"\)/\1$new_desc\2/" ${NEW_TEST}.tmp > $NEW_TEST
    rm ${NEW_TEST}.tmp
done