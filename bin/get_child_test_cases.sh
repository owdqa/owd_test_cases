#!/bin/bash

TYPE=${1:?"Syntax: $0 <test type>"}

U=$(egrep "^U" $HOME/.jira_login | awk '{print $2}')
P=$(egrep "^P" $HOME/.jira_login | awk '{print $2}')

#
# Parameters for Jira items.
#
[ ! "$USER_STORIES_BASEURL" ] && export USER_STORIES_BASEURL="https://jirapdi.tid.es/browse/OWD-"

#
# Get the jira id's for test cases.
#
HERE=$(dirname $0)
. $HERE/jira_test_cases.sh

#
# Different types of 'type'.
#
x=$(echo "$TYPE" | egrep "^[0-9]*$")
if [ "$x" ]
then
	# This is already a parent id.
	ROOTIDs=$TYPE
else
    case $TYPE in
    	
    	"REGRESSION")  
    	   #
    	   # Run 'everything'.
    	   #
    	   for i in "${JIRA_PARENTS[@]}"
           do
               $0 $(echo "$i" | awk '{print $1}')
           done;;
           
        "SMOKE")  
           #
           # Run smoketests.
           #
           # NOT SET UP YET, WE NEED THE JIRA PARENT ID FOR THIS!!!
           ROOTIDs="";;
           
        *)
           #
           # Run all test cases for this particular type.
           #           
           for i in "${JIRA_PARENTS[@]}"
           do
               PARENT=$(echo "$i" | awk '{print $1}')
               if [ "$PARENT" = "$TYPE" ]
               then
               	    PARENTID=$(echo "$i" | awk '{for (i=2;i<=NF;++i)printf "%s ", $i; printf "\n"}')
                    ROOTIDs="$PARENTID"
                    break
               fi
           done;;
           
    esac
fi

[ ! "$ROOTIDs" ] && exit

#
# We may have more than one ROOTID for this type ...
#
for ROOTID in $(echo "$ROOTIDs")
do
	#
	# Go to JIRA and get the ids (requires you to be in the intranet or VPN).
	#
	wget -O /tmp/root_jira_issue.html \
	     --no-check-certificate       \
	     --user=$U --password=$P      \
	     ${USER_STORIES_BASEURL}${ROOTID}?os_authType=basic >/dev/null 2>&1
	
	#
	# Strip out the numbers from the html.
	#
	awk 'BEGIN{
	    FOUND = ""
	    while ( getline < "/tmp/root_jira_issue.html" ){
	
	        if ( $0 ~ /dt title="is tested by/ ){ FOUND = "Y" }
	
	        if ( $0 ~ /div id="show-more-links"/ ){ break }
	
	        if ( $0 ~ /span title="OWD-/ ){
	            x = $0
	            gsub(/^.*span title=\"OWD-/, "", x)
	            gsub(/:.*$/, "", x)
	            print x
	        }
	    }
	}'
done

