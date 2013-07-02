#!/bin/bash

TYPE=${1:?"Syntax: $0 <test type>"}

U=$(egrep "^U" $HOME/.jira_login | awk '{print $2}')
P=$(egrep "^P" $HOME/.jira_login | awk '{print $2}')

ROOTID=""
case "$TYPE" in
    "CONTACTS") ROOTID=27032;;
    "FTU"     ) ROOTID=27067;;
    "DIALLER" ) ROOTID=27004;;
    "MMS"     ) ROOTID=27003;;
    "SMS"     ) ROOTID=26940;;
esac

[ ! "$ROOTID" ] && exit

wget -O /tmp/root_jira_issue.html --no-check-certificate --user=$U --password=$P https://jirapdi.tid.es/browse/OWD-${ROOTID}?os_authType=basic >/dev/null 2>&1

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


