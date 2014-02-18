#!/bin/sh
### BEGIN INIT INFO
# Provides:          develenv-18
# Short-Description: Start/stop
# chkconfig: 2345 86 14
# description: Start, stops develenv-18
### END INIT INFO
#
# develenv       This init.d script is used to start develenv.


ENV="env -i LANG=C PATH=/usr/local/bin:/usr/bin:/bin"
DEVELENV_HOME=/home/develenv
DEVELENV_USER=develenv
. $DEVELENV_HOME/bin/setEnv.sh

$INIT_FUNCTIONS

case $1 in
    start)
        $SCRIPT_LOG_METHOD_DAEMON "Starting develenv-18"
        $DEVELENV_HOME/bin/sumarize.sh start
        $DEVELENV_HOME/bin/startupAll.sh
    ;;
    stop)
        $SCRIPT_LOG_METHOD_DAEMON "Stopping develenv-18"
        $DEVELENV_HOME/bin/shutdownAll.sh
    ;;
    restart)
        $SCRIPT_LOG_METHOD_DAEMON "Restarting develenv-18"
        $SCRIPT_LOG_METHOD_DAEMON "Stopping develenv-18"
        $DEVELENV_HOME/bin/shutdownAll.sh
        $SCRIPT_LOG_METHOD_DAEMON "Starting develenv-18"
        $DEVELENV_HOME/bin/startupAll.sh
    ;;

    *)
        $SCRIPT_LOG_METHOD_SUCESS "Usage: /etc/init.d/$0 {start|stop|restart}"
        exit 1
    ;;
esac
