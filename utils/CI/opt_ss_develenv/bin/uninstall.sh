#!/bin/bash
function currentDir(){
   DIR=`readlink -f $0`
   DIR=`dirname $DIR`
}
function killProject(){
   service develenv stop
   DIR_OLD_PROJECT=$PWD
   if [ -d  "$PROJECT_HOME" ]; then
      cd $PROJECT_HOME 2>/dev/null
      if [ "$?" == "0" ]; then
         ISALIFE=`cat develenv.pid`
         cd $DIR_OLD_PROJECT
         if [ "$ISALIFE" != "" ]; then
            kill -9 $ISALIFE 2>/dev/null
         fi
      fi
      ISALIFE=`ps -ef|grep "org.apache.catalina.startup.Bootstrap"|grep "$PROJECT_USER"|cut -d' ' -f2`
      ISALIFE2=`ps -ef|grep "org.apache.catalina.startup.Bootstrap"|grep "$PROJECT_USER"|cut -d' ' -f3`
      if [ "$ISALIFE" != "" ]; then
         kill -9 $ISALIFE 2>/dev/null
      fi
      if [ "$ISALIFE2" != "" ]; then
         kill -9 $ISALIFE2 2>/dev/null
      fi
   fi
   # Matando todos los procesos java presentes para el usuario develenv
   if [ "`grep "^$PROJECT_USER\:" /etc/passwd`" != "" ]; then
      su $PROJECT_USER -c "killall -9 java 2>/dev/null"
   fi
}
function removeProject(){
   killProject
   rm -Rf $APACHE_CONF_DIR/$PROJECT_NAME*.conf $APACHE_CONF_DIR/conf.d/${PROJECT_NAME}.conf.d /etc/httpd/conf.d/develenv.conf.d
   if [ -f "/etc/init.d/$APACHE2_SCRIPT_INIT" ]; then
      service $APACHE2_SCRIPT_INIT reload
   fi
   #Se intenta desactivar el servicio independientemente de que esté activado
   $BOOT_COMMAND_UNDO 2>&1 >/dev/null
   if [ "$yumInstallation" != "true" ]; then
      rm -Rf /home/$PROJECT_USER
      rm -Rf /var/$PROJECT_NAME
      rm -Rf /var/tmp/$PROJECT_NAME
      rm -Rf /var/log/$PROJECT_NAME
      rm -Rf /etc/$PROJECT_NAME
      rm -Rf /etc/init.d/$PROJECT_NAME
      rm -Rf /opt/${ORG_ACRONYM}/$PROJECT_NAME
      rm -Rf /etc/yum/repos.d/${ORG_ACRONYM}-thirdparty-${APPNAME}*.*
   fi
   rm -Rf $APACHE_CONF_DIR/$PROJECT_NAME*.conf $APACHE_CONF_DIR/conf.d/${PROJECT_NAME}.conf.d 
   [ -z "`cat /proc/version|grep \"Red Hat\"`" ] && rm -Rf /etc/apache2/conf.d/${APPANAME}.conf /etc/apache2/conf.d/${APPANAME}.conf.d /etc/httpd/
   if [ -f "/etc/init.d/$APACHE2_SCRIPT_INIT" ]; then
      service $APACHE2_SCRIPT_INIT reload
   fi
   #Borrando link httpd a apache para versiones Debian
   userdel -f $PROJECT_USER 2>/dev/null
}
currentDir
. $DIR/setEnv.sh
isRPMinstallation
installationIn${distribution}
removeProject
