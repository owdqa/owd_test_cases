#!/bin/sh
. /home/develenv/bin/setEnv.sh
_log "\n
+++++++++++++++++++++++++++++++
   Parando develenv
+++++++++++++++++++++++++++++++"

su - develenv -c "$PROJECT_HOME/bin/shutdownTomcat.sh"
$PROJECT_HOME/platform/selenium/bin/selenium.sh stop
#Remove Xvfb
kill -9 `cat /tmp/.X20-lock`
rm -Rf /tmp/.X20-lock












