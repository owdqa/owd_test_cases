#!/bin/bash
#
# Takes you to the /tmp/tests directory for the latest build - use ". $0" to run this.
#

# Get the latest run dir.
cd /tmp/tests

dirnam=$(ls -lrtd * | tail -1 | awk '{print $NF}')
cd $dirnam
