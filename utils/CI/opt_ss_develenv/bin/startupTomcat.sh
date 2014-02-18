#!/bin/sh
. /home/develenv/bin/setEnv.sh

_log "\n
#####################
   Inicializando Tomcat
#####################"
OLD_DIR=$PWD
cd $PROJECT_HOME/platform/tomcat/bin
CATALINA_BASE=""
CATALINA_HOME=""
TOMCAT_HOME=""
if [ -f $PROJECT_HOME/develenv.pid ]; then
   PID=`cat $PROJECT_HOME/develenv.pid`
   exists=`ps -ef|grep java|grep $PID`
   if [ "$exists" != "" ]; then
       kill -9 $PID
   fi
   rm -Rf $PROJECT_HOME/develenv.pid
fi

./startup.sh
cd $OLD_DIR


