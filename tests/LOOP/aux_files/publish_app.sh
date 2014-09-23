#!/bin/bash
MY_PATH=`pwd`
cd ~/firefoxos-loop-client && git fetch && git merge origin/master

cd $MY_PATH/loop-to-market
./pack_and_upload.sh
