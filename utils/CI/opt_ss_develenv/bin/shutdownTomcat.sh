#!/bin/sh
. /home/develenv/bin/setEnv.sh

_log "\n
#####################
   Parando Tomcat
#####################"
$PROJECT_HOME/platform/tomcat/bin/shutdown.sh

