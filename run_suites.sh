#!/bin/bash
export DATE=`date +"%Y%m%d"`
export RESULTS_DIR="$HOME/Escritorio/RESULTS/SCRIPT/PUBLIC/testrun_$DATE"

mkdir -p $RESULTS_DIR

for suite in "$@"
do
    ./run_tests.sh $suite
    cp -r /tmp/tests/test_123 $RESULTS_DIR/$suite
done
