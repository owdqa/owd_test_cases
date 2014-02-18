from CSVParser import *

# This parameter specifies the ROWS of previous data that we have to skip before
# the CSV file starts
ROWS_TO_JUMP = 1

# It is necessary to specify the labels of our CSS so that it can be processed right
labels = ["TEST_SUITE","BUILD_NUMBER","DEVICE","VERSION","BUILD_BEING_TESTED",
"URL_RUN_DETAILS","START_TIME","END_TIME","TEST_CASES_PASSED","UNEXPECTED_FAILURES",
"AUTOMATION_FAILURES","UNEX_PASSES","EX_FAILS","EX_PASSES","IGNORED","UNWRITTEN",
"PERCENT_PASSED"]

# CSV file to be processed
file = 'total_csv_file.csv'

# We just have to call to our super parser, stating the file, the labels, and the rows
# to be skipped
parser = CSVParser(file, labels, ROWS_TO_JUMP)

# FILTER PROCESS: This labels are gonna be the ones to be erased from the file
filterLabels = ["TEST_SUITE", "BUILD_NUMBER", "VERSION", "DEVICE", "URL_RUN_DETAILS", "TEST_CASES_PASSED",
                    "AUTOMATION_FAILURES"]
parser.filterColumns(filterLabels)


# parser.filterRows({"BUILD_NUMBER": "==20"})
parser.filterRows({"VERSION": "v1.2"})
#WRITE PROCESS: just specify the path to the file. It does not have to exist
parser.write("./myfile.CSV")

