#!/bin/bash
#
# Tails the latest realtime logfile from our ci run so you can
# see how far through it is.
#
$HOME/bin/roy/goto_latest_run_dir.sh

tail -f realtime_summary
