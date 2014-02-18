#!/usr/bin/env bash

directorioTest=${1:-.}

listaDIRS=`ls -l $directorioTest | grep "^d" | awk '{print $9}'`

for dir in $listaDIRS;
do
	numero=`ls ${directorioTest}/${dir}/ | grep ".*.py" | wc -l`
	echo "El directorio "${dir}" tiene "${numero}" tests "
done
