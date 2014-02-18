#!/bin/bash
function currentDir(){
   DIR=`readlink -f $0`
   DIR=`dirname $DIR`
}
TEMP_DIR=/home/develenv/temp/rpms
mkdir -p $TEMP_DIR
SPEC_FILE="$TEMP_DIR/thirdparty-develenv-repo.spec"
lineSeparator=`grep -n "###### SPEC ######" $0|grep -v "grep" |sed s:"\:###### SPEC ######":"":g`
sed 1,${lineSeparator}d $0 > $SPEC_FILE
rpmbuild -v  --clean  --define '_topdir '$TEMP_DIR --define 'major_version '1 --define 'minor_version '0 --define 'major_release '0 --define 'minor_release '0 -bb $SPEC_FILE
mkdir -p  /home/develenv/app/repositories/rpms/noarch/
mv /home/develenv/temp/rpms/RPMS/noarch/develenv-repo*.* /home/develenv/app/repositories/rpms/noarch/
createrepo -s sha -d --update /home/develenv/app/repositories/rpms/noarch/
rm -Rf $TEMP_DIR

exit 0
###### SPEC ######

%define _builddir %{_topdir}/BUILD

%define _rpm_name %{name}-%{version}-%{release}
%define _debug_dir /home/develenv/temp/rpms/debug/%{_rpm_name}
%define _log echo -e [`date '+%Y-%m-%d %X'`] [%{_rpm_name}]
%define _log_init "==== Init ===="
%define _log_prep %{_log} [PREP]
%define _log_prep_init  %{_log_prep} %{_log_init}  ;%{__mkdir_p} %{_debug_dir}; env >%{_debug_dir}/env_prep;%{__cp} $0 %{_debug_dir}/prep
%define _log_clean %{_log} [CLEAN]
%define _log_clean_init %{_log_clean}  ;%{__mkdir_p} %{_debug_dir}; find ${RPM_BUILD_ROOT} -name "*" >%{_debug_dir}/buildroot;env >%{_debug_dir}/env_clean;%{__cp} $0 %{_debug_dir}/clean
%define _log_build %{_log} [BUILD]
%define _log_build_init %{_log_build} %{_log_init} ;%{__mkdir_p} %{_debug_dir}; env >%{_debug_dir}/env_build;%{__cp} $0 %{_debug_dir}/build
%define _log_install %{_log} [INSTALL]
%define _log_install_init %{_log_install} %{_log_init} ;%{__mkdir_p} %{_debug_dir}; env >%{_debug_dir}/env_install;%{__cp} $0 %{_debug_dir}/instSPall
%define _log_pre %{_log} [PRE-INSTALL]
%define _log_pre_init %{_log_pre} %{_log_init} ;%{__mkdir_p} %{_debug_dir}; env >%{_debug_dir}/env_pre_install;%{__cp} $0 %{_debug_dir}/pre_install
%define _log_post %{_log} [POST-INSTALL]
%define _log_post_init %{_log_post} %{_log_init} ;%{__mkdir_p} %{_debug_dir}; env >%{_debug_dir}/env_post_install;%{__cp} $0 %{_debug_dir}/post_install

%define _log_preun %{_log} [PRE-UNINSTALL]
%define _log_preun_init %{_log_preun} %{_log_init} ;%{__mkdir_p} %{_debug_dir}; env >%{_debug_dir}/env_pre_uninstall;%{__cp} $0 %{_debug_dir}/pre_uninstall

%define _log_postun %{_log} [POST-UNINSTALL]
%define _log_postun_init %{_log_postun} %{_log_init} ;%{__mkdir_p} %{_debug_dir}; env >%{_debug_dir}/env_post_uninstall;%{__cp} $0 %{_debug_dir}/post_uninstall



# repo spec file
#
#
Name: ss-thirdparty-develenv-repo
Summary:   Repository rpms
Version:   %{major_version}.%{minor_version}
Release:   %{major_release}.%{minor_release}
Packager:  SoftwareSano
Group:     None
BuildArch: noarch
License:   http://develenv.softwaresano.com/license.html
Vendor:    SoftwareSano
URL:       http://develenv.softwaresano.com
Requires:  wget


%define component_home /etc/yum.repos.d
%define yum_repos_dir  %{component_home}


%description
thirdparty-develenv repository

%prep
%{_log_prep_init}

%{_log_prep} Building package %{name}-%{version}
[ -d $RPM_BUILD_ROOT/%{component_home} ] || %{__mkdir_p} $RPM_BUILD_ROOT/%{component_home}

   
%build
%{_log_build_init}


%install
%{_log_install_init}

getHostname(){
        IP=`LANG=C /sbin/ifconfig | grep "inet addr" | grep "Bcast" | awk '{ print $2 }' | awk 'BEGIN { FS=":" } { print $2 }' | awk ' BEGIN { FS="." } { print $1 "." $2 "." $3 "." $4 }'`
   MAC_ADDRESSES=`LANG=C /sbin/ifconfig -a|grep HWaddr|awk '{ print $5 }'`
        if [ -z "$IP" ]; then
            echo -e "\nNo hay conexión de red. Introduce el nombre o la ip de la máquina: \c"
            read HOST
        else
          j=0
          for i in $IP;
             do
              #Averiguamos si alguna IP tiene asignada nombre de red
         j=$(($j +1 ));
              temp=`LANG=C nslookup $i|grep "name = "|cut -d= -f2| sed 's/.//' | sed 's/.$//'`
              if [ "$temp" != "" ]; then
                 HOST=$temp
                 INTERNALIP=$i
       MAC_ADDRESS=`echo $MAC_ADDRESSES|cut -d' ' -f$j`
              fi
          done
          if [ -z "$HOST" ]; then
             # Probablemente sea una conexión wifi, y no tenga asignada un nombre en el DNS
             HOST=`hostname`
             INTERNALIP=`echo $IP|cut -d' ' -f1`
        MAC_ADDRESS=`echo $MAC_ADDRESSES|cut -d' ' -f1`
             # Si no hay un nombre de hosts asignado
        if [ -z "$HOST" ];then
                # Nos quedamos con la primera IP
           HOST=$INTERNALIP
        fi
          fi
        fi
}

cd ${RPM_BUILD_ROOT}/%{component_home}
getHostname
NOTA="# Repositorio de rpms generados con thirdparty-develenv
# NOTA: Si el acceso a thirdparty-develenv es desde una red diferente
#       Comprueba que la url (baseurl) es accesible desde la máquina
#       donde se instala este rpm. En caso de que se modifique la URL
#       antes de instalar un paquete borrar el contenido del directorio
#       /var/cache/yum/ (rm -Rf /var/cache/yum/*)
"
architectures="noarch i686 x86_64 src"
for architecture in $architectures; do
    echo "
$NOTA
[thirdparty-develenv-$architecture]
name=thirdparty-develenv-$architecture
baseurl=http://thirdparty-develenv-softwaresano.googlecode.com/svn/trunk/develenv/src/site/resources/tools/rpms/$architecture
enabled=1
gpgcheck=0" > thirdparty-develenv-repo-$architecture.repo
done;



%clean
%{_log_clean_init}

[ -d $RPM_BUILD_ROOT/%{component_home} ] || %{__mkdir_p} $RPM_BUILD_ROOT/%{component_home}



%files
%attr (-,root,root) %{component_home}
%config  %{component_home}

%pre
%{_log_pre_init}


%post
%{_log_post_init}
if [ "`arch`" == "x86_64" ]; then
   %{__rm} -Rf %{component_home}/thirdparty-develenv-repo-i686.repo
else
   %{__rm} -Rf %{component_home}/thirdparty-develenv-repo-x86_64.repo
fi
wget `cat %{component_home}/thirdparty-develenv-repo-noarch.repo|grep "baseurl="|sed s:"baseurl=":"":g`/repodata/repomd.xml -O repomd.xml.tmp
if [ "$?" != 0 ]; then
   echo Los repositorios han sido instalados correctamente. Pero la URL `cat %{component_home}/thirdparty-develenv-repo-noarch.repo|grep "baseurl="|sed s:"baseurl=":"":` no es accesible. Revise que son accesibles las urls de los ficheros %{component_home}/thirdparty-develenv-repo-*.repo.
fi
rm -Rf repomd.xml.tmp
%{_log_post} Remove cache rpm directory
%{__rm} -Rf %{_var}/yum/cache/*

%preun
%{_log_preun_init}

%postun
%{_log_postun_init}

%{_log_postun} Remove cache rpm directory
%{__rm} -Rf %{_var}/yum/cache/*



