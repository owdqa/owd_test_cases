#!/bin/bash
#
# Shows test id and desc for tests we don't have.
#
BASE_URL="https://jirapdi.tid.es/browse/OWD-"
USER_STORY_ID=${1:?"Usage: $0 <user story id>"}

TMP=/tmp/jira_test_cases_for_${USER_STORY_ID}
export WGET_OUTPUT=${TMP}.html
export RESULT_FILE=${TMP}.result

U=$(egrep "^U" ~/.jira_login 2>/dev/null| awk '{print $2}')
P=$(egrep "^P" ~/.jira_login 2>/dev/null| awk '{print $2}')

U=${U:?"Could not find USERNAME in $HOME/.jira_login!"}
P=${P:?"Could not find PASSWORD in $HOME/.jira_login!"}



#
# Get the report html into a temporary file.
#
wget -O ${WGET_OUTPUT} --no-check-certificate ${BASE_URL}${USER_STORY_ID}?os_authType=basic --user=$U --password=$P >/dev/null 2>&1

#
# Now the messy part ... get the test numbers and descriptions from the html tables.
#
awk '
BEGIN{
	WGET_OUTPUT = ENVIRON["WGET_OUTPUT"]
	TEST_NUM    = ""
	TEST_DESC   = ""
	TEST_CASE   = ""
	TD_COUNT    = 0
	TD_DESC     = 4
	
	INTC = ""
	while (getline < WGET_OUTPUT){
		
		if ( $0 ~ /span title="OWD-/ ) INTC = "Y"

		if ( INTC == "" ) continue
		
		x = $0
		gsub(/^.*span title="OWD-/, "", x)
		gsub(/: /, "|", x)
		gsub(/">.*$/, "", x)
		print x
		
		if ( $0 ~ /">/ ) INTC = ""
	}
}' > $RESULT_FILE

cat $RESULT_FILE | while read line
do
    TESTID=$(echo "$line" | awk 'BEGIN{FS="|"}{print $1}')
    DESC=$(  echo "$line" | awk 'BEGIN{FS="|"}{print $2}')

    x=$(find . -name test_${TESTID}.py)
    if [ ! "$x" ]
    then
        echo "($TESTID) $DESC"
    fi
done
