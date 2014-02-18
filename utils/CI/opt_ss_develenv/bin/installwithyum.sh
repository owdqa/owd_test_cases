#!/bin/bash
function currentDir(){
   DIR=`readlink -f $0`
   DIR=`dirname $DIR`
}


function help(){
   echo Uso: $0 -Dadmnistrator.id=[administrator] -Dpassword=[password] [-Dmultienviroment] [-Dorg=[organization]] [--help]
   echo "Configuración paquete $PROJECT_NAME"
   echo ""
   echo ""
   echo "OPCIONES:"
   echo "    -Dadministrator.id Usuario administrador para jenkins(http://$HOSTNAME/jenkins)  y para la administración de $PROJECT_NAME(http://$HOSTNAME/admin)"
   echo "    -Dpassword Password para la administración de $PROJECT_NAME(http://$HOSTNAME/admin)"
   echo "    -Dorg=[url] Url con los parámetros de configuración de la organización donde se instala $PROJECT_NAME"
   echo "          Ej: -Dorg=http://develenv.googlecode.com/svn/${URL_DEVELENV_REPO}/src/main/filters/softwaresano.properties Configura $PROJECT_NAME con los parámetros de Softwaresano"
   echo "    --help: Esta pantalla de ayuda."
   echo ""
   echo "EJEMPLO:"
   echo "    $0 -Dadministrator.id=$PROJECT_NAME -Dpassword=$PROJECT_NAME"
   echo ""
   echo "Más información en http://develenv.softwaresano.com/docs/installation.html"
}


function installPackages(){
   . ./setEnv.sh
   [ "$yumInstallation" == "true" ] && return true
   installationIn${distribution}
   echo $CONFIGURE_REPOS >configureRepos.sh
   chmod 755 configureRepos.sh
   ./configureRepos.sh
   rm -Rf configureRepos.sh
   $INSTALL_PACKAGE $NEW_PACKAGES -y
   if [ "$?" != 0 ]; then
      echo "[ERROR] No se pueden instalar los paquetes ${NEW_PACKAGES}. Puede que no haya conexión a internet o quizás haya que configurar el proxy para acceder a internet."
      exit 1
   fi
   $APACHE2_MODULES
}
# No todas las distribuciones añaden el hostname al /etc/hosts.  Para evitar problemas se añade
function addHostnameToEtcHost(){
       #Si no se ha añadido el hostname al /etc/hosts se añade
       if ! [ -z "$HOSTNAME" ]; then
          if [ -z "`cat /etc/hosts|grep -w \"\( |\t\)*$HOSTNAME\( |\t|$\)*\"`" ]; then
             echo -e "127.0.0.1\t$HOSTNAME" >> /etc/hosts
          fi
       fi
}
function installRedHat(){
      installationInRedHat
      if [ -f "/etc/sysconfig/iptables" ]; then
         isRHFirewall=`cat /etc/sysconfig/iptables|grep "\-A RH-Firewall"`
         if ! [ -z $isRHFirewall ]; then
            ENABLED_HTTP=`cat /etc/sysconfig/iptables|grep "\-A RH-Firewall-1-INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT"`
            if [ "$ENABLED_HTTP" == "" ]; then
               sed -i s:"-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT":"-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT\n-A RH-Firewall-1-INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT":g /etc/sysconfig/iptables
            fi
         else
            ENABLED_HTTP=`cat /etc/sysconfig/iptables|grep "\-A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT"`
            if [ "$ENABLED_HTTP" == "" ]; then
               sed -i s:" --dport 22 -j ACCEPT":" --dport 22 -j ACCEPT\n-A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT":g /etc/sysconfig/iptables
            fi
         fi
         service iptables restart
      fi
      service mysqld restart
      chkconfig httpd on
      chkconfig mysqld on
      # Para que funciona el firefox sin X
      ! [ -f "/var/lib/dbus/machine-id" ] && dbus-uuidgen --ensure
}

function installDebian(){
   installationInDebian
   service apache2 restart
   JAVA_HOME=${java_dir}

   if [ `uname -m` == "x86_64" ]; then
           PACKAGES_INSTALLATION=""
   else
      PACKAGES_INSTALLATION=""
   fi
   if [ "$PACKAGES_INSTALLATION" != "" ]; then
      wget $PACKAGES_INSTALLATION
      dpkg -i *.deb
      rm -Rf *.deb
      apt-get clean
   fi
}

function configureSelinux(){
   #Configure selinux
   echo "[Start] Selinux configuration"
   #http://wiki.centos.org/HowTos/SELinux (5.1) Relabeling files
   chcon -Rv --type=httpd_sys_content_t /var/$PROJECT_NAME/
   chcon -Rv --type=httpd_sys_content_t /var/log/$PROJECT_NAME
   chcon -Rv --type=httpd_sys_content_t /etc/$PROJECT_NAME
   #Redirect apache tomcat
   /usr/sbin/setsebool -P httpd_can_network_connect 1 
}

function postInstallRedHat(){
   #Permitimos la redirección apache a tomcat
   echo "[Start] RedHat PostInstallation"
   configureSelinux
   echo "[Finish] RedHat PostInstallation"
}
function postInstallDebian(){
   #nothing
   echo "[Start] Debian PostInstallation"
   rm -Rf /etc/yum.repos.d
   echo "[Finish] Debian PostInstallation"
}

function linksToConfigurations(){
   toolName="$1"
   toolDir="$2"
   su $PROJECT_USER -c "mkdir -p `dirname \"$toolDir\"` && cd `dirname \"$toolDir\"` && ln -s /etc/$APPNAME/$toolName/ `basename \"$toolDir\"`"
}


function configureLinks(){
   su $PROJECT_USER -c "cd $PROJECT_HOME && ln -s /opt/ss/$APPNAME/bin && ln -s /opt/ss/$APPNAME/platform && ln -s /opt/ss/$APPNAME/README && ln -s /opt/ss/$APPNAME/RELEASE_NOTES && ln -s /opt/ss/$APPNAME/LICENSE && ln -s /opt/ss/$APPNAME/install"
   su $PROJECT_USER -c "cd $PROJECT_HOME && ln -s /var/$APPNAME/docs docs"
   su $PROJECT_USER -c "mkdir -p $PROJECT_HOME/app/ && cd $PROJECT_HOME/app/ && ln -s /var/$APPNAME/$SITES $SITES"
   su $PROJECT_USER -c "cd $PROJECT_HOME/app/ && ln -s /var/$APPNAME/repositories repositories"
   su $PROJECT_USER -c "cd $PROJECT_HOME/app/ && ln -s /var/$APPNAME/maven maven"
   su $PROJECT_USER -c "cd $PROJECT_HOME/platform/tomcat && ln -s /var/log/$APPNAME/tomcat logs"
   linksToConfigurations "tomcat" "$PROJECT_HOME/platform/tomcat/conf/"
   linksToConfigurations "nexus" "$PROJECT_HOME/sonatype-work/nexus/conf/"
   su $PROJECT_USER -c "cd /var/$APPNAME/nexus/ && mkdir -p indexer proxy storage timeline"
   su $PROJECT_USER -c "cd $PROJECT_HOME/sonatype-work/nexus && ln -s /var/$APPNAME/nexus/indexer && ln -s /var/$APPNAME/nexus/proxy && ln -s /var/$APPNAME/nexus/storage && ln -s /var/$APPNAME/nexus/timeline && ln -s /var/$APPNAME/nexus/plugin-repository"
   su $PROJECT_USER -c "cd $PROJECT_HOME/sonatype-work/nexus && mkdir -p /var/log/$APPNAME/nexus && ln -s /var/log/$APPNAME/nexus logs"
   su $PROJECT_USER -c "mkdir -p $PROJECT_HOME/app/nexus/ && cd $PROJECT_HOME/app/nexus/ && ln -s $PROJECT_HOME/sonatype-work"
   su $PROJECT_USER -c "mkdir -p $PROJECT_HOME/app/jenkins && cd $PROJECT_HOME/app/ && ln -s jenkins hudson"
   su $PROJECT_USER -c "mkdir -p /var/$APPNAME/jenkins/fingerprints /var/$APPNAME/jenkins/updates /var/$APPNAME/jenkins/userContent && cd $PROJECT_HOME/app/jenkins/ && ln -s /var/$APPNAME/jenkins/fingerprints && ln -s /var/$APPNAME/jenkins/updates && ln -s  /var/$APPNAME/jenkins/userContent"
   su $PROJECT_USER -c "cd $PROJECT_HOME/app/jenkins && ln -s /var/$APPNAME/jenkins/jobs jobs"
   su $PROJECT_USER -c "cd $PROJECT_HOME/app/jenkins && ln -s /var/$APPNAME/jenkins/plugins plugins"
   su $PROJECT_USER -c "cd $PROJECT_HOME/app/jenkins && ln -s /var/$APPNAME/jenkins/users users"
   su $PROJECT_USER -c "mkdir -p /var/log/$APPNAME/jenkins && cd $PROJECT_HOME/app/jenkins/ && ln -s /var/log/$APPNAME/jenkins log"
   ### START: configuration links
   linksToConfigurations "jenkins" "$PROJECT_HOME/app/jenkins/" 
   pushd . >/dev/null
   cd $PROJECT_HOME/app/jenkins
   for jenkinsConfFile in `find "/etc/$APPNAME/jenkins" -name "*.xml"`; do
      su $PROJECT_USER -c "ln -s $jenkinsConfFile"
   done;
   popd >/dev/null
   su $PROJECT_USER -c "ln -s $PROJECT_HOME/app/jenkins/ $PROJECT_HOME/.jenkins"
   su $PROJECT_USER -c "ln -s $PROJECT_HOME/app/jenkins/ $PROJECT_HOME/.hudson"
   linksToConfigurations "sonar" "/var/$APPNAME/sonar/conf/"
   linksToConfigurations "maven" "$PROJECT_HOME/platform/maven/conf/"
   linksToConfigurations "maven2" "$PROJECT_HOME/platform/maven2/conf/"
   ### END: configuration links
   su $PROJECT_USER -c "cd $PROJECT_HOME && ln -s /etc/$APPNAME conf"
   su $PROJECT_USER -c "mkdir -p /var/log/$APPNAME/sonar && cd /var/$APPNAME/sonar && ln -s /var/log/$APPNAME/sonar logs"
   su $PROJECT_USER -c "mkdir -p $PROJECT_HOME/app/ && cd $PROJECT_HOME/app/ && ln -s /var/$APPNAME/sonar"
   su $PROJECT_USER -c "cd $PROJECT_HOME && ln -s /var/log/$APPNAME logs"
   su $PROJECT_USER -c "cd $PROJECT_HOME/app/repositories && ln -s /var/$APPNAME/nexus/storage nexus"
   su $PROJECT_USER -c "mkdir -p $PROJECT_HOME/app/repositories/nexus/groups && cd $PROJECT_HOME/app/repositories/nexus/groups && ln -s /var/$APPNAME/nexus/storage/public public"
   su $PROJECT_USER -c "cd $PROJECT_HOME/app/repositories/nexus/groups && ln -s /var/$APPNAME/nexus/storage/public-snapshots public-snapshots"
   su $PROJECT_USER -c "mkdir -p /var/$APPNAME/plugins && cd $PROJECT_HOME/app && ln -s /var/$APPNAME/plugins"
   su $PROJECT_USER -c "mkdir -p /var/$APPNAME/temp && cd $PROJECT_HOME && ln -s /var/$APPNAME/temp"
   # Apache
   [ -z "`cat /proc/version|grep \"Red Hat\"`" ] && pushd . && cd /etc/apache2/conf.d && rm -Rf $APPNAME.conf && rm -Rf ${APPNAME}.conf.d && ln -s /etc/httpd/conf.d/${APPNAME}.conf && ln -s /etc/httpd/conf.d/${APPNAME}.conf.d && popd
   su $PROJECT_USER -c "cd $PROJECT_HOME/conf && ln -s /etc/httpd/conf.d/${APPNAME}.conf.d/ apache"
}


function installDevelenvPlugins(){
   cd $PROJECT_HOME/bin
   echo Instalando plugins de $PROJECT_HOME
   ./installPlugin.sh python_plugin http://develenv-python-plugin.googlecode.com/files/python_plugin-12.dp
   ./installPlugin.sh php_plugin http://develenv-php-plugin.googlecode.com/files/php_plugin-12.dp
   ./installPlugin.sh pipeline_plugin http://develenv-pipeline-plugin.googlecode.com/svn/tags/pipeline_plugin-11/
   #Cpp plugin sólo esta testeado en distribuciones debian
   if [ "$distribution" == "Debian" ]; then #
      ./installPlugin.sh cpp_plugin http://develenv-cpp-plugin.googlecode.com/files/cpp_plugin-12.dp
   fi

}

function defaultInstallation(){
   echo -e "================================================================================"
   echo -e "\n $PROJECT_NAME puede instalarse con las opciones por defecto (administrator.id=$PROJECT_NAME password=$PROJECT_NAME )"
   echo -e "\n¿Deseas instalar $PROJECT_NAME con las opciones por defecto? (s/n): \c"
   read ANSWER
   case $ANSWER in
      'S'|'s'|'')
            $0 -Dadministrator.id=$PROJECT_NAME -Dpassword=$PROJECT_NAME
            exit $?
      ;;
       'N'|'n')
            exit 0
           ;;
       *)  echo "Debes teclar s ó n"y
      exit 1
   esac
}


function areYouSure(){
   echo -e "\n¿Estás seguro que quieres desinstalar $PROJECT_NAME? (S/n): \c"
   read ANSWER
   case $ANSWER in
      'S'|'s'|'')
         echo "Eliminando $PROJECT_NAME-$PROJECT_VERSION  "
         $DIR/uninstall.sh
      ;;
      'N'|'n')
         echo "Desinstalación $PROJECT_NAME-$PROJECT_VERSION cancelada"
         exit 2
      ;;
       *)  echo "Debes teclar s ó n"
      exit 1
   esac
}

function getHostname(){
   IP=`LANG=C /sbin/ifconfig | grep "inet addr" | grep "Bcast" | awk '{ print $2 }' | awk 'BEGIN { FS=":" } { print $2 }' | awk ' BEGIN { FS="." } { print $1 "." $2 "." $3 "." $4 }'`
   MAC_ADDRESSES=`LANG=C /sbin/ifconfig -a|grep HWaddr|awk '{ print $5 }'`
   if [ "$IP" == "" ]; then
      echo -e "\nNo hay conexión de red. Introduce el nombre o la ip de la máquina: \c"
      read HOST
   else
      local j=0
      for i in $IP; do
         #Averiguamos si alguna IP tiene asignada nombre de red
         j=$(($j +1 ));
         temp=`LANG=C nslookup $i|grep "name = "|cut -d= -f2| sed 's/.//' | sed 's/.$//'`
         if [ "$temp" != "" ]; then
            HOST=$temp
            INTERNALIP=$i
            MAC_ADDRESS=`echo $MAC_ADDRESSES|cut -d' ' -f$j`
         fi
      done
      if [ "$HOST" == "" ]; then
         # Probablemente sea una conexión wifi, y no tenga asignada un nombre en el DNS
         HOST=`hostname`
         INTERNALIP=`echo $IP|cut -d' ' -f1`
         MAC_ADDRESS=`echo $MAC_ADDRESSES|cut -d' ' -f1`
         # Si no hay un nombre de hosts asignado
         if [ "$HOST" == "" ];then
            # Nos quedamos con la primera IP
            HOST=$INTERNALIP
         fi
      fi
   fi
}

function getParameter(){
   count=1
   value=""
   until [ "$*" == "" ] 
   do
      parameter=$1
      shift
      count=`expr $count + 1`
      if [ "$value" == "" ]; then
         if [ "${parameter:0:${#param}}" == "${param}" ]; then
            value=${parameter:${#param}}
         fi
      fi
   done
}

function getOrganization(){
   param="-Dorg="
   getParameter $*
   if [ "$value" != "" ]; then
     echo $value|egrep "http://|https://:|ftp://|file://"
     curl $value  > $PROJECT_HOME/install/conf/default_organization.properties
     if [ "$?" != 0 ]; then
        echo "[ERROR] No se encuentra el fichero de configuración $value"
        exit 1
     fi
     organization=""
     profileorg="-Dorg=default_organization"
   fi
}

function getAdministratorId(){
    param="-Dadministrator.id="
    getParameter $*
    administratorId=$value
}

function getPassword(){
    param="-Dpassword="
    getParameter $*
    passwordAdmin=$value
}
function internetAccess(){
   # Comprobando la conexión a internet
   if [ -z $LOCAL_SOFTWARESANO ]; then
      curl http://www.softwaresano.com 1>/dev/null 2>/dev/null
      if [ "$?" != "0" ]; then
         echo "No hay acceso a internet"
         exit 1
      fi
   fi
}

function isRPMinstallation(){
   yumInstallation="false"
}

function isJavaOk(){
   [ "$yumInstallation" == "true" ] && JAVA_HOME="/usr/java/default" && return 0
   if [ "$distribution" != "Debian" ]; then
      if [ "$JAVA_HOME" == "/usr/java/default" ]; then
         echo "No está definida la variable JAVA_HOME"
         help
         return 1
      fi
      temp=`find "$JAVA_HOME/bin" -name "javac"`
      if [ "$temp" == "" ]; then
         echo "En la ubicación $JAVA_HOME/bin/javac no existe la máquina virtual de java"
         return 1
      fi
   fi
   return true
}

function uninstall(){
   [ "$yumInstallation" == "true" ] && return true
   ###
   # Desinstalando cualquier version anterior
   # Si ya estaba instalado se desinstala
   if [ -d "/home/$PROJECT_USER" ]; then
      areYouSure
   else
      $DIR/uninstall.sh
   fi
}

function createUser(){
   useradd $PROJECT_USER
   if [ "$?" != "0" ]; then
      echo "El usuario $PROJECT_USER ya existe. Para todos los procesos asociados al usuario \"$PROJECT_USER\" y bórralo"
      exit 1
   fi
   sed -i s:"$PROJECT_HOME\:/bin/sh":"$PROJECT_HOME\:/bin/bash":g /etc/passwd
}

function decompress(){
   [ "$yumInstallation" == "true" ] && return true
   createUser
   FILE_TAR_GZ=$PROJECT_NAME-$PROJECT_VERSION-install.tar.gz
   cd /

   echo "Descomprimiendo $FILE_TAR_GZ..."
   tar xfz $DIR/$FILE_TAR_GZ
   if [ "$?" != 0 ]; then
      echo "Error en la descompresión de $FILE_TAR_GZ"
      exit 1
   fi
   rm -Rf xfz $DIR/$FILE_TAR_GZ
   chown -R $PROJECT_USER:$PROJECT_USER /var/$APPNAME
   chown -R $PROJECT_USER:$PROJECT_USER /var/log/$APPNAME
   chown -R $PROJECT_USER:$PROJECT_USER /etc/$APPNAME
   chown -R $PROJECT_USER:$PROJECT_USER /etc/httpd/conf.d/${APPNAME}.conf.d
   chown -R $PROJECT_USER:$PROJECT_USER /home/$APPNAME
   chown -R $PROJECT_USER:$PROJECT_USER /opt/ss/$APPNAME
   chown -R $PROJECT_USER:$PROJECT_USER /etc/yum.repos.d/${ORG_ACRONYM}-thirdparty-${APPNAME}*
}

function deleteUnnecessaryFiles(){
   # Se borran los ficheros utilizados temporalmente para realizar la instalación
   rm -Rf $PROJECT_HOME/install
   rm -Rf $PROJECT_HOME/bin/configure*.sh
   rm -Rf $PROJECT_HOME/bin/installSonarDB.sh
   rm -Rf $PROJECT_HOME/bin/rpmRepo.sh
   rm -Rf $PROJECT_HOME/bin/apacheAutoIndex.sh
   cd $ORIGINAL_DEVELENV_DIR
   rm -Rf $PROJECT_HOME/.adminDevelenv
}
function postInstall(){
   cd $PROJECT_HOME
   echo "Configurando Links"
   configureLinks
   mkdir -p $prefix/install/conf
   cp -R $DIR/conf/* $prefix/install/conf
   cd $prefix/bin
   current_time=`date +%T`
   crond="`date -u -d$current_time-0015 '+%M %H'`"
   getOrganization $*
   echo "Configurando $PROJECT_NAME ..."
   if [ -z $LOCAL_SOFTWARESANO ]; then
      INSTALL_DIR_LOG=/var/log/$APPNAME
   else
      INSTALL_DIR_LOG=/tmp
   fi
   su $PROJECT_USER -c "../platform/ant/bin/ant -l $INSTALL_DIR_LOG/${PROJECT_NAME}.log -buildfile $PROJECT_HOME/install/buildfile \
            -Ddevelenv.host=$HOSTNAME -Ddevelenv.port="" \
            -Ddevelenv.prefix="$prefix" -Denv=$enviroment \
            -Ddevelenv.crond=\"$crond\" \
            -Ddevelenv.projectName=$PROJECT_NAME \
            -Ddevelenv.projectVersion=$PROJECT_VERSION \
            -Ddevelenv.projectHome=$PROJECT_HOME \
            -Ddevelenv.java.home=$JAVA_HOME replaceUser $* $profileorg >$INSTALL_DIR_LOG/${PROJECT_NAME}.error.log"
   if [ "$?" != "0" ]; then
      echo "Error durante la personalización."
      echo "Revisa $INSTALL_DIR_LOG/${PROJECT_NAME}.error.log y $INSTALL_DIR_LOG/${PROJECT_NAME}.log"
      exit 1
   fi
   su $PROJECT_USER -c "../platform/ant/bin/ant -l $INSTALL_DIR_LOG/${PROJECT_NAME}.1.log -buildfile $PROJECT_HOME/install/buildfile \
            -Ddevelenv.host=$HOSTNAME -Ddevelenv.port="" \
            -Ddevelenv.prefix="$prefix" -Denv=$enviroment \
            -Ddevelenv.projectName="$PROJECT_NAME" \
            -Ddevelenv.projectVersion="$PROJECT_VERSION" \
            -Ddevelenv.projectHome=$PROJECT_HOME \
            -Ddevelenv.crond=\"$crond\" \
            -Ddevelenv.java.home=$JAVA_HOME $* $profileorg >$INSTALL_DIR_LOG/${PROJECT_NAME}.1.error.log"
   if [ "$?" != "0" ]; then
      echo "Error durante la personalización."
      echo "Revisa $INSTALL_DIR_LOG/${PROJECT_NAME}.error.1.log y $INSTALL_DIR_LOG/${PROJECT_NAME}.log"
      exit 1
   fi

   find ../ -name "*.sh" -exec chmod 755 {} \;
   . ./setEnv.sh

   ./configureApache.sh

   /etc/init.d/$APACHE2_SCRIPT_INIT reload
   ./installSonarDB.sh
   su $PROJECT_USER -c ./rpmRepo.sh
   rm -Rf /etc/init.d/$PROJECT_NAME
   ln -s $PROJECT_HOME/bin/bootstrap.sh /etc/init.d/$PROJECT_NAME
   $BOOT_COMMAND
   chmod 755 /home/$PROJECT_USER
   pushd . >/dev/null
   cd $PROJECT_HOME/docs/$PROJECT_GROUPID/$PROJECT_NAME
   $PROJECT_HOME/bin/apacheAutoIndex.sh
   popd >/dev/null
   # To publish develenv parameters first time
   mkdir -p `dirname $FIRST_EXECUTION_FILE`
   touch $FIRST_EXECUTION_FILE
   touch $PROJECT_HOME/.adminDevelenv
   installDevelenvPlugins
   postInstall${distribution}
   deleteUnnecessaryFiles
   service $PROJECT_NAME start
   echo $PROJECT_NAME instalado.
   getAdministratorId $*
   getPassword $*
   echo -e "================================================================================"
   echo "Los usuarios/password para $PROJECT_NAME son:"
   echo "Admin ${PROJECT_NAME}:"
   echo "   Usuario=${administratorId} "
   echo "   Password=${passwordAdmin}"
   echo "   Role=Administrador de tomcat"
   echo "   Url=http://$HOSTNAME/$PROJECT_NAME/admin/"
   echo "Jenkins:"
   echo "   Usuario=${administratorId} "
   echo "   Password=${passwordAdmin} ó Si se ha configurado un LDAP para el acceso a Jenkins será el password que haya definido en LDAP"
   echo "   Role= Administrador de jenkins"
   echo "   Url=http://$HOSTNAME/jenkins"
   echo "Nexus:"
   echo "   Usuario=${administratorId}"
   echo "   Password=develenv  ó Si se ha configurado un LDAP para el acceso a Nexus será el password que haya definido en LDAP"
   echo "   Role=Administrador de nexus"
   echo "   Url=http://$HOSTNAME/nexus"
   echo "Sonar:"
   echo "   Usuario=${administratorId}"
   echo "   Password=develenv ó Si se ha configurado un LDAP para el acceso a Sonar será el password que haya definido en LDAP"
   echo "   Role= Administrador de sonar"
   echo "   Url=http://$HOSTNAME/sonar"
   echo "Selenium Grid:"
   echo "   Url=http://$HOSTNAME/grid"
   echo "$PROJECT_NAME: Manuales de $PROJECT_NAME"
   echo "   Usuario=anonymous"
   echo "   Password="
   echo "   Url=http://$HOSTNAME/docs"
   echo "Logs de $PROJECT_NAME "
   echo "   Usuario=anonymous"
   echo "   Password="
   echo "   Descripción=Acceso a los logs de $PROJECT_NAME"
   echo "   Url=http://$HOSTNAME/$PROJECT_NAME/logs"
   echo "Configuración de $PROJECT_NAME"
   echo "   Usuario=anonymous"
   echo "   Password="
   echo "   Descripción=Acceso en modo lectura a los ficheros de configuración de $PROJECT_NAME"
   echo "   Url=http://$HOSTNAME/$PROJECT_NAME/config"
   echo "Guía de administración de $PROJEC_NAME:"
   echo "   Url=http://$HOSTNAME/docs/administrationGuide.html"
   echo "Repositorios de componentes:"
   echo "   Usuario=anonymous"
   echo "   Password="
   echo "   Url=http://$HOSTNAME/$PROJECT_NAME/repos"
   echo "   Descripción=Repositorios con los componentes(maven, rpms, debian, ...) generados por los diferentes jobs de jenkins"
   echo "[NOTAS]"
   echo "  [1] El arranque de $PROJECT_NAME puede tardar varios minutos debido al arranque de sonar. Esto significa que durante el arranque al acceder a cualquier herramienta de $PROJECT_NAME, el servidor devolverá 'Service Temporarily Unavailable' "
   echo "  [2] En  http://code.google.com/p/develenv-plugins/ existe una lista con los plugins disponibles para $PROJECT_NAME (PHP, android, ...)"
   echo "  [3] En  http://code.google.com/p/develenv/wiki/newProject existe una guía para desarrollar tú primer proyecto con $PROJECT_NAME"
   echo "  [4] Las herramientas que componen develenv(sobre todo jenkins y sonar) utilizan plugins para ampliar la funcionalidad de las mismas. Estos plugins pueden consumir bastante memoria. Si develenv no arranca comprobar la memoria que queda libre en la máquina utilizando el comando free -m"
   echo "  [5] Consulta las últimas versiones disponibles de $PROJECT_NAME en http://develenv.softwaresano.com"
   echo "  [6] Cualquier error/sugerencia sobre develenv enviar un mail a develenv@softwaresano.com"
}

currentDir
. $DIR/setEnv.sh
ORIGINAL_DEVELENV_DIR=$PWD
OLD_DIR=$PWD
isRPMinstallation
[[ -z `echo $PROJECT_VERSION|egrep "\-SNAPSHOT$"` ]] && URL_DEVELENV_REPO="tags/develenv-${PROJECT_VERSION}" || URL_DEVELENV_REPO="trunk/develenv"
organization=`echo $*|grep "\-Dorg"`

help=`echo $*|grep "\-\-help"`
if [ -n "$help" ]; then
        help
        exit 1
fi
for parameter in $*;
    do
    temp=`echo $parameter |grep  "\-Dadministrator.id="|cut -d '=' -f2`
    if [ -n "$temp" ]; then
       administratorId=$temp
    fi
    temp=`echo $parameter |grep  "\-Dpassword="|cut -d '=' -f2`
    if [ -n "$temp" ]; then
       password=$temp
    fi
done
allParameters=true
if [ "$administratorId" == "" ]; then
   echo "Falta definir el administrador de $PROJECT_NAME"
   allParameters=false
fi
if [ "$password" == "" ]; then
   echo "Falta el password para el administrador de $PROJECT_NAME"
   allParameters=false
fi
if [ "$allParameters" == "false" ]; then
   help
   defaultInstallation
   exit $?
fi


#################
# Es necesario ser root para instalar este develenv
if [ "`id|grep \"uid=0\"`" == "" ]; then
   echo "Para instalar $PROJECT_NAME es necesario ser root"
   exit 2
fi
isJavaOk
[ $? != 0 ] && exit 1

if [ "$prefix" == "" ]; then
   prefix=/home/$PROJECT_NAME
fi

addHostnameToEtcHost
internetAccess
echo "Configurando "
getHostname
echo "Compilación para la máquina $HOSTNAME"
enviroment=native

uninstall

if [ "$organization" == "" ]; then
   profileorg="-Dorg=default_organization"
fi
# Instalando paquetes
installPackages
install$distribution
prefix=/home/$PROJECT_USER
PROJECT_HOME=$prefix
decompress
postInstall $*
exit 0
