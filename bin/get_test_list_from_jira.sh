#!/bin/bash
#
# Collects a list of test id's and descriptions from JIRA.
#
# NOTE: The report must be in the 'cache' (i.e. via quick link).
#
BASE_URL="http://qacore02.hi.inet/sites/jira/reports/user-story-coverage-OWD-Regression_Automated_"
BRANCH=${1:?"Syntax: $0 <branch>"}

export TMPFILE=/tmp/jira_report_${BRANCH}.html

#
# Get the report html into a temporary file.
#
wget -O ${TMPFILE} --no-check-certificate ${BASE_URL}${BRANCH}.html > /dev/null 2>&1

if [ $? -ne 0 ]
then
	printf "\nReport for \"$BRANCH\" wasn't in the 'cache' in JIRA - please manually run the report in JIRA then try this again.\n\n"
    exit 1
fi

#
# Now the messy part ... get the test numbers and descriptions from the html tables.
#
awk '
BEGIN{
	TMPFILE   = ENVIRON["TMPFILE"]
	TEST_NUM  = ""
	TEST_DESC = ""
	TEST_CASE = ""
	TD_COUNT  = 0
	TD_DESC   = 4
	
	while (getline < TMPFILE){
		if ( /<td>Test Case<\/td>/ ){
			# We are in a test case.
			TEST_CASE = "Y"
		}
		
		if ( TEST_CASE == "Y" && /href.*jirapdi.tid.es\/browse\/OWD/ ){
			# This contains the test number.
            TD_COUNT  = 1
            TEST_DESC = ""
			TEST_NUM  = $0
            gsub(/^.*>OWD-/, "", TEST_NUM)
            gsub(/<.*$/    , "", TEST_NUM)
            continue
		}
		
		if ( TD_COUNT > 0 && /<td/ ){
			# We are in a test case - increment the td counter.
			TD_COUNT = TD_COUNT + 1
		}
		
        if ( TD_COUNT == TD_DESC ){
            # We are in the test description (can cover a few lines).
            TEST_DESC = TEST_DESC $0
            gsub(/<td>/  , "" , TEST_DESC)
            gsub(/<\/td>/, "" , TEST_DESC)
            gsub(/^ */   , "" , TEST_DESC)
            gsub(/  */   , " ", TEST_DESC)
        }

        if ( TD_COUNT == TD_DESC && /<\/td/ ){
        	# We are at the end of a description TD.
        	TD_COUNT  = 0
        	TEST_CASE = ""
        	printf "%s\t%s\n", TEST_NUM, TEST_DESC
        }
	}
}'
