#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#

class test_main(GaiaTestCase):
    
    _day_num  = 0
    _day_name = ""
 
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.calendar   = Calendar(self)
        
        
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.calendar.launch()
        
        #===================================================================================================
        #
        # MONTH view
        #
        self.calendar.moveMonthViewBy(1)
        self.calendar.moveMonthViewBy(-1)
        self.calendar.moveMonthViewBy(5)
        self.calendar.moveMonthViewBy(-5)

        #===================================================================================================
        #
        # WEEK view
        #
        self.calendar.moveWeekViewBy(1)
        self.calendar.moveWeekViewBy(-1)
        self.calendar.moveWeekViewBy(5)
        self.calendar.moveWeekViewBy(-5)
 
        #===================================================================================================
        #
        # DAY view
        #
        self.calendar.moveDayViewBy(1)
        self.calendar.moveDayViewBy(-1)
        self.calendar.moveDayViewBy(5)
        self.calendar.moveDayViewBy(-5)
