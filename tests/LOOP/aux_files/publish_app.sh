#!/bin/bash
MY_PATH=$PWD
cd $1 && git fetch && git merge origin/master

cd $MY_PATH/loop-to-market
./pack_and_upload.sh
