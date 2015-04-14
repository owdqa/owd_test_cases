#!/bin/bash
export DATE=`date +"%Y%m%d"`
export RESULTS_DIR="/home/alberto/Escritorio/RESULTS/PUBLIC/testrun_$DATE"

mkdir -p $RESULTS_DIR

for suite in "$@"
do
    echo "Running suite $suite..."
    python ../OWD_TEST_TOOLKIT/scripts/ffox_test_runner.py --testvars=../OWD_TEST_TOOLKIT/config/gaiatest_testvars.json --address=localhost:2828  --restart tests/$suite
    cp -r /tmp/tests/ $RESULTS_DIR/$suite
done
