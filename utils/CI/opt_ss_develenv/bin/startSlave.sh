#!/bin/bash
. /home/develenv/bin/setEnv.sh
$JAVA_HOME/bin/java -jar $PROJECT_HOME/platform/tomcat/webapps/jenkins/WEB-INF/slave.jar -jnlpUrl http://$1/jenkins/computer/`hostname`/slave-agent.jnlp
