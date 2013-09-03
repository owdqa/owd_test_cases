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
        _now = self.UTILS.getDateTimeFromEpochSecs(int(time.time()))
        
        #
        # Launch contacts app.
        #
        self.calendar.launch()
        
        self.calendar.setView("month")
        self.calendar.setView("today")
        
        #
        # Check month view details are correct for 'today'.
        #
        x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Header")
        _expected_str = "%s %s" % (_now.month_name, _now.year)
        self.UTILS.TEST(_expected_str.lower() in x.text.lower(), 
                        "Header: '%s' contains today's details ('%s')." % (x.text, _expected_str))
        
        x = self.UTILS.getElement(DOM.Calendar.mview_selected_day_title, "Selected day detail string")
        _expected_str = "%s %s %s %s" % (_now.day_name, _now.mday, _now.month_name, _now.year)
        self.UTILS.TEST(_expected_str.lower() in x.text.lower(), 
                        "Day detail string: '%s' contains today's details ('%s')." % (x.text, _expected_str))
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)