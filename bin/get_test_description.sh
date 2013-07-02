#!/bin/bash

OUTFILE=/tmp/roytest
BASE_URL="https://jirapdi.tid.es/browse/OWD-"

I=${1:?"Syntax: $0 <JIRA issue>"}
U=$(egrep "^U" ~/.jira_login 2>/dev/null| awk '{print $2}')
P=$(egrep "^P" ~/.jira_login 2>/dev/null| awk '{print $2}')

U=${U:?"Could not find USERNAME in $HOME/.jira_login!"}
P=${P:?"Could not find PASSWORD in $HOME/.jira_login!"}

wget -O $OUTFILE --no-check-certificate ${BASE_URL}${I}?os_authType=basic --user=$U --password=$P >/dev/null 2>&1

DESC=$(grep "<title>" $OUTFILE | sed -e "s/^.*\][ \t]*\(.*\) - Jira.*$/\1/")
DESC=${DESC:-"(No description found in ${BASE_URL}${I})"}

echo "$DESC"
