#!/bin/bash
MYNAME=$(basename $0)
OUTFILE=/tmp/$MYNAME.log
BASE_URL="https://jirapdi.tid.es/browse/OWD-"

rm -rf $OUTFILE 2>/dev/null

I=${1:?"Syntax: $0 <JIRA issue>"}
U=$(egrep "^U" ~/.jira_login 2>/dev/null| awk '{print $2}')
P=$(egrep "^P" ~/.jira_login 2>/dev/null| awk '{print $2}')

U=${U:?"Could not find USERNAME in $HOME/.jira_login!"}
P=${P:?"Could not find PASSWORD in $HOME/.jira_login!"}

wget -O $OUTFILE --no-check-certificate ${BASE_URL}${I}?os_authType=basic --user=$U --password=$P >/dev/null 2>&1

DESC=$(grep "<title>" $OUTFILE | sed -e "s/^.*\][ \t]*\(.*\) - Jira.*$/\1/")
DESC=${DESC:-"(Unable to get description from ${BASE_URL}${I})"}

#
# This &#39; character is what is returned by wget if there is a " ' " in the description.
# It messes up our description in the tets details files, so change it back with sed.
#
echo "$DESC" | sed -e "s/&#39;/'/g" | sed -e "s/&quot;/'/g"
