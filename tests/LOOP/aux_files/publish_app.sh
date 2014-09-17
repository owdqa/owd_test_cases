#!/bin/bash
MY_PATH=`pwd`
cd ~/firefoxos-loop-client && git fetch && git merge origin/master

cd $MY_PATH/loop-to-store
./pack_and_upload.sh
