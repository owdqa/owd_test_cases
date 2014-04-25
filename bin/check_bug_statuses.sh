#!/bin/bash
#
# A standalone executable to return a list of blocking bugs who's statuses are now marked as RESOLVED.
#
export LOGFILE=/tmp/tmp_bug_statuses.html
BUGZILLA_URL="https://bugzilla.mozilla.org/show_bug.cgi?id="
BLOCK_FILE=$(dirname $0)/../Docs/blocked_tests
DESCS_FILE=$(dirname $0)/../Docs/test_descriptions

#
# Set the expected string to look for, for our branch.
#
BRANCH=$(git branch | awk '{print $NF}')
case $BRANCH in
    "1.0.1"    ) export BRANCH_STR="status-b2g18-v1.0.1"; export COMMENT_BRANCH_STR="v1.0.1";;
	"v1-train" ) export BRANCH_STR="status-b2g18"       ; export COMMENT_BRANCH_STR="v1-train";;
    "1.1"      ) export BRANCH_STR="status-b2g-v1.1hd"  ; export COMMENT_BRANCH_STR="master";;
    "v1.2"     ) export BRANCH_STR="status-b2g-v1.2"    ; export COMMENT_BRANCH_STR="v1.2";;
    "v1.3"     ) export BRANCH_STR="status-b2g-v1.3"    ; export COMMENT_BRANCH_STR="v1.3";;
    "v1.4"     ) export BRANCH_STR="status-b2g-v1.4"    ; export COMMENT_BRANCH_STR="v1.4";;
esac

echo "
Checking the status of any bugzilla bugs that are currently 'blocking' OWD automated test cases ...
"
    
UNBLOCK_LIST=$(for BUGID in $(egrep -v "^#" $BLOCK_FILE | awk 'BEGIN{FS="|"}{print $NF}' | sed -e "s/[^0-9 ]*//g" | sort -u)
do
	export BUGID
	
	TESTLIST=""
	while read testcase
	do
		test_desc=$(egrep "^$testcase\|" $DESCS_FILE | awk 'BEGIN{FS="|"}{print $NF}')
		if [ "$TESTLIST" ]
        then
        	TESTLIST="$TESTLIST
          ($testcase) $test_desc"
        else
            TESTLIST="($testcase) $test_desc"
	    fi
	done <<EOF
	$(grep $BUGID $BLOCK_FILE | awk 'BEGIN{FS="|"}{print $1}' | sort -u)
EOF

    export TESTLIST
	
    #
    # Go to the bug and get the html.
    #
    wget -O $LOGFILE --no-check-certificate ${BUGZILLA_URL}${BUGID} >/dev/null 2>&1
         
    #
    # Strip out the reuired parts from the html.
    #
    awk 'BEGIN{
    	LOGFILE                 = ENVIRON["LOGFILE"]
    	BUGID                   = ENVIRON["BUGID"]
    	TESTLIST                = ENVIRON["TESTLIST"]
    	BRANCH_STR              = ENVIRON["BRANCH_STR"]
    	COMMENT_BRANCH_STR      = ENVIRON["COMMENT_BRANCH_STR"]
        IN_DESC                 = ""
        DESC                    = ""
        IN_TRACKING_FLAGS_TABLE = ""
        IN_LABEL                = ""
        LABEL                   = ""
        STATUS                  = ""
        COMMENT_NUM             = "(unknown)"

        while ( getline < LOGFILE ){
        	
            #
            # Deal with the DESCRIPTION.
            #
            if ( $0 ~ /span *id="short_desc_nonedit_display"/ ){
            	IN_DESC = "Y" 
            	DESC    = $0
            }
            
            if ( IN_DESC != "" ) {
	            
	            gsub(/^.*span *id="short_desc_nonedit_display"[^>]*>/, "", DESC)
	            gsub(/<\/span>.*$/, "", DESC)
	            gsub(/&quot;/, "\"", DESC)
	            
	            if ( $0 ~ /<\/span>/ ){
	            	IN_DESC = ""
	            }
            }
            
            #
            # GATHER INFO ON THE STATUS (USING THE FLAG FIELD).
            #
            if ( $0 ~ /table *class="tracking_flags"/ ){
                IN_TRACKING_FLAGS_TABLE = "Y"
            }
            
            if ( IN_TRACKING_FLAGS_TABLE != "" && $0 ~ /<label .*status/ ){
                LABEL = $0
                gsub(/^.*<label.*>/, "", LABEL)
                gsub(/:/, "", LABEL)
                if ( LABEL == BRANCH_STR ){
                	IN_LABEL = "Y"
                }
            }
            
            if ( IN_TRACKING_FLAGS_TABLE != "" && IN_LABEL != "" && $0 ~ /<td>/ ) {
                IN_STATUS = "Y"
                STATUS = $0
                gsub(/^.*<td.*>/, "", STATUS)
                break
            }

            if ( IN_TRACKING_FLAGS_TABLE != "" && $0 ~ /<\/table>/ ) {
            	IN_TRACKING_FLAGS_TABLE = ""
            }
            
            #
            # ... trying comments.
            #
            if ( $0 ~ /href=".*">Comment [0-9]*<\/a>/ ){
            	COMMENT_NUM = $0
                gsub(/^.*Comment */, "", COMMENT_NUM)
                gsub(/<\/a>.*/, "", COMMENT_NUM)
            }
            if ( $0 ~ /<pre *class="bz_comment_text"/ ){
            	X = $0
            	gsub(/<pre *class="bz_comment_text" *>/, "", X)
            	gsub(/:.*$/, "", X)
            	if ( X == COMMENT_BRANCH_STR ){
            		STATUS = "(fix for \"" COMMENT_BRANCH_STR "\" mentioned in comment " COMMENT_NUM ".)"
            		break
            	}
            }
        }
        
        if ( STATUS ~ /.*RESOLVED.*/ || STATUS ~ /.*fixed.*/ || STATUS ~ /fix for/ ){
            gsub(/&quot;/, "\"", TESTLIST)
            
            printf "\n"
            printf "\nBUG     : %s", BUGID
            printf "\nDESC    : %s", DESC
            printf "\nSTATUS  : %s", STATUS
            printf "\nBLOCKING: %s", TESTLIST
            printf "\n"
        }
    }'
done)

if [ "$UNBLOCK_LIST" ]
then
	echo "

The following 'blocking' bugs are now marked as RESOLVED in bugzilla, so it may be possible to unblock the tests associated with them:
$UNBLOCK_LIST

"

    #
    # Exit as failed so this will always be emailed by Jenkins.
    #
    exit 1
else
    echo "
    
None of the 'blocking' bugs are marked as RESOLVED in bugzilla at this time.

"
fi
