export DATE=`date +"%Y%m%d"`
export RESULTS_DIR="$HOME/Desktop/RESULTS/SCRIPT/PUBLIC/testrun_$DATE"

mkdir -p $RESULTS_DIR

for suite in "$@"
do
    python ../OWD_TEST_TOOLKIT/scripts/ffox_test_runner.py --address=localhost:2828 --testvars=../OWD_TEST_TOOLKIT/config/gaiatest_testvars.json --log-tbpl=/tmp/tests/tests.log tests/$suite
    cp -r /tmp/tests $RESULTS_DIR/$suite
done