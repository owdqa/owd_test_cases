#!/bin/sh
. ./setEnv.sh

service develenv stop
sleep 10
_log "[INFO] Eliminando ficheros temporales de tomcat"
rm -Rf $PROJECT_HOME/platform/tomcat/logs/* $PROJECT_HOME/platform/tomcat/temp/* $PROJECT_HOME/platform/tomcat/work/* $PROJECT_HOME/platform/conf/Catalina
service develenv start







