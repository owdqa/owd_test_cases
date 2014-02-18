#!/bin/bash
. /home/develenv/bin/setEnv.sh
selenium="on"
_log "\n
+++++++++++++++++++++++++++++++
   Inicializando develenv
+++++++++++++++++++++++++++++++"
[ -f "/home/develenv/.adminDevelenv" ] && echo "[ERROR] develenv isn't started because now is updating" && exit 1
su - develenv -c "Xvfb :20 -ac -screen 0 1024x768x8 2>/dev/null &"
su - develenv -c "export DISPLAY=\":20.0\";. $PROJECT_HOME/bin/setEnv.sh;$PROJECT_HOME/bin/startupTomcat.sh"
[ "$selenium" == "on" ] && $PROJECT_HOME/platform/selenium/bin/selenium.sh start
#Para el caso de que se utilice un proxy para el acceso a internet comentar la línea anterior y configurar el proxy en la siguiente linea.
#su - develenv -c "export http_proxy=http://carlosg:mipassword@proxy.softwaresano.com;export DISPLAY=":20.0";$PROJECT_HOME/bin/startupTomcat.sh"

