#!/bin/bash
# Warning: Error control is for sissies. If you haven't configured the .config first
# and this explodes and erases something you don't have a backup for, well, it sucks to
# be you, I guess. You have my more sincere simpathies. Or not ;)

function reportError() {
    echo $1 1>&2
    exit 1
}

cd `dirname $0`
MY_PATH=`pwd`
TMP_DIR=${MY_PATH}/tmpout.$$

source ./.config

mkdir $TMP_DIR

cd $LOOP_LOCATION || reportError "Hmm... $LOOP_LOCATION doesn't seem to exist"

grunt release || reportError "grunt didn't work as expected. Is 'grunt release' working on ${LOOP_LOCATION}?"

cd $MY_PATH || reportError "WTF! Why can't I go to $MY_PATH"

APP_FILE=${TMP_DIR}/application.zip

cp ${LOOP_LOCATION}/application.zip ${APP_FILE}

cd $TMP_DIR || reportError "Cannot cd to ${TMP_DIR}"
unzip application.zip manifest.webapp

# Hey, a comment! :P We have to scp the zip and manifest first...
FILE_TMPL=${APP_OWNER}_${APP_UUID}${APP_SUFFIX}
DST_TMPL=owdStore/uploadedApps${STORE_SUFFIX}/${FILE_TMPL}

echo "Copying files to owdstore.hi.inet..."
(scp -i ${SSH_ID} application.zip stageUsr@owdstore.hi.inet:${DST_TMPL}.zip &&
  scp -i ${SSH_ID} manifest.webapp stageUsr@owdstore.hi.inet:${DST_TMPL}.webapp) ||
  reportError "There was an error copying the files!"
echo "Done copying. Hopefully"

cd ${MY_PATH} && rm -rf $TMP_DIR

#And now that the file is copied, let's sign it
URL_COMMON="https://owdstore.hi.inet/${STORE}/admMarket"
curl -v -k -c ./cookie.jar.$$ -u "${WEB_CREDENTIALS}" ${URL_COMMON}/publishAppP1.html >./curl_log.$$ 2>&1
CSRFCOOKIE=`grep csrftoken ./cookie.jar.$$ | cut  -f 7`
curl -v -k -b ./cookie.jar.$$ -e "${URL_COMMON}/publishAppP1.html" -d "csrfmiddlewaretoken=${CSRFCOOKIE}&pass=${SIGN_PASSWORD}&fileName=${FILE_TMPL}.webapp" -u "${WEB_CREDENTIALS}" ${URL_COMMON}/publishAppP2.html >>./curl_log.$$ 2>&1

rm ./cookie.jar.$$

(grep "Application ${APP_OWNER}_${APP_UUID} correctly published" ./curl_log.$$ && rm -f ./curl_log.$$) ||
  reportError "There was an error publishing. Check previous lines and the $MY_PATH/curl_log.$$ file for errors"

echo "And all done, hopefully."
