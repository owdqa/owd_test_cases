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
#         #
#         self.calendar.moveMonthViewBy(1)
#         self.calendar.moveMonthViewBy(-1)
#         self.calendar.moveMonthViewBy(5)
#         self.calendar.moveMonthViewBy(-5)

        #===================================================================================================
        #
        # WEEK view
        #
        self.calendar.moveWeekViewBy(1)
        return

        #===================================================================================================
        #
        # DAY view
        #
        self.calendar.setView("day")
        
        self.UTILS.logResult("info", "<b>Testing <i>day</i> view for <i>today</i> ...</b>")
        self.calendar.setView("today")
        self._day_num   = _now.mday
        self._day_name  = _now.day_name
        self._dayViewTests(_now)
         
        self._getNewDay(_now, "day")
        self._dayViewTests(_now)



    def _dayViewTests(self, p_now):
        x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Day view header")

        self.UTILS.TEST(self._day_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (self._day_name, x.text))
        
        self.UTILS.TEST(p_now.month_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (p_now.month_name, x.text))
        
        self.UTILS.TEST(str(self._day_num) in x.text,
                        "'%s' is in the header ('%s')." % (self._day_num, x.text))
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot in day view with 'today' selected:", x)
        
        
    def _weekViewTests(self, p_now):
        x = self.UTILS.getElements(DOM.Calendar.wview_active_days, "Active days")
        _testStr = "%s %s" % (self._day_name[:3], self._day_num)
        boolOK = False
        for i in x:
            if _testStr.lower() in i.text.lower():
                boolOK = True
                break
        self.UTILS.TEST(boolOK, "Selected day is displayed")
        
        x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Week view header")
        self.UTILS.TEST(p_now.month_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (p_now.month_name, x.text))
        
        self.UTILS.TEST(str(p_now.year) in x.text,
                        "'%s' is in the header ('%s')." % (p_now.year, x.text))
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot in week view with 'today' selected:", x)
        
        
    def _monthViewTests(self, p_now):
        # Highlighted cell is correct ...
        el_id_str = "d-%s-%s-%s" % (p_now.year, p_now.mon-1, self._day_num)
        self.UTILS.waitForElements( ("xpath", 
                                    "//li[@data-date='%s' and contains(@class, 'selected')]" % el_id_str),
                                  "Selected day for %s/%s/%s" % (self._day_num, p_now.mon, p_now.year), True, 2, False)

        # Selected day string is correct ...
        x = self.UTILS.getElement(DOM.Calendar.mview_selected_day_title, "Selected day detail string")
        _expected_str = "%s %s %s %s" % (self._day_name, self._day_num, p_now.month_name, p_now.year)
        self.UTILS.TEST(_expected_str.lower() in x.text.lower(), 
                        "Day detail string: '%s' contains today's details ('%s')." % (x.text, _expected_str))
        
        x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Month view header")
        self.UTILS.TEST(p_now.month_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (p_now.month_name, x.text))
        
        self.UTILS.TEST(str(p_now.year) in x.text,
                        "'%s' is in the header ('%s')." % (p_now.year, x.text))
                
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot in month view with 'today' selected:", x)



    def _getNewDay(self, p_now, p_numDays, p_viewType):
        #
        # Private function to get a diffrent day (avoiding issues with month and week).
        #
        _days   = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        self._day_num = (p_now.mday - p_numDays)
        if  self._day_num < 1:
            self._day_num = 28 - (p_numDays - p_now.mday)
                    
        self._day_name = (p_now.wday - p_numDays)
        if  self._day_name < 1:
            self._day_name = 6 - (p_numDays - p_now.wday)
                    
        self.UTILS.logResult("info", "<b>Testing <u>%s</u> view for <i>%s day(s) in the past</i> ...</b>" % \
                             (p_viewType, _numdays))

        #
        # Switch to month view and tap this day, then switch back to our view.
        #
        self.calendar.setView("month")
        el_id_str = "d-%s-%s-%s" % (p_now.year, p_now.mon-1, self._day_num)
        x = self.UTILS.getElement( ("xpath", 
                                    "//li[@data-date='%s']" % el_id_str),
                                  "Cell for day %s/%s/%s" % (self._day_num, p_now.mon, p_now.year))
        x.tap()
        self.calendar.setView(p_viewType)
