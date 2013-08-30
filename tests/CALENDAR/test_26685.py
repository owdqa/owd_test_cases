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
        _now = self.UTILS.getDateTimeFromEpochSecs(int(time.time()))
        
        #
        # Launch contacts app.
        #
        self.calendar.launch()
        
        #===================================================================================================
        #
        # MONTH view
        #
        self.calendar.setView("month")
         
        self.UTILS.logResult("info", "<b>Testing <i>month</i> view for <i>today</i> ...</b>")
        self.calendar.setView("today")
        self._day_num   = _now.mday
        self._day_name  = _now.day_name
        self._monthViewTests(_now)
         
        self._getNewDay(_now, "month")
        self._monthViewTests(_now)

        #===================================================================================================
        #
        # WEEK view
        #
        self.calendar.setView("week")
        
        self.UTILS.logResult("info", "<b>Testing <i>week</i> view for <i>today</i> ...</b>")
        self.calendar.setView("today")
        self._day_num   = _now.mday
        self._day_name  = _now.day_name
        self._weekViewTests(_now)
         
        self._getNewDay(_now, "week")
        self._weekViewTests(_now)

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


    def _dayViewTests(self, _now):
        x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Day view header")

        self.UTILS.TEST(self._day_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (self._day_name, x.text))
        
        self.UTILS.TEST(_now.month_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (_now.month_name, x.text))
        
        self.UTILS.TEST(str(self._day_num) in x.text,
                        "'%s' is in the header ('%s')." % (self._day_num, x.text))
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot in day view with 'today' selected:", x)
        
        
    def _weekViewTests(self, _now):
        x = self.UTILS.getElements(DOM.Calendar.wview_active_days, "Active days")
        _testStr = "%s %s" % (self._day_name[:3], self._day_num)
        boolOK = False
        for i in x:
            if _testStr.lower() in i.text.lower():
                boolOK = True
                break
        self.UTILS.TEST(boolOK, "Selected day is displayed")
        
        x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Week view header")
        self.UTILS.TEST(_now.month_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (_now.month_name, x.text))
        
        self.UTILS.TEST(str(_now.year) in x.text,
                        "'%s' is in the header ('%s')." % (_now.year, x.text))
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot in week view with 'today' selected:", x)
        
        
    def _monthViewTests(self, _now):
        # Highlighted cell is correct ...
        el_id_str = "d-%s-%s-%s" % (_now.year, _now.mon-1, self._day_num)
        self.UTILS.waitForElements( ("xpath", 
                                    "//li[@data-date='%s' and contains(@class, 'selected')]" % el_id_str),
                                  "Selected day for %s/%s/%s" % (self._day_num, _now.mon, _now.year), True, 2, False)

        # Selected day string is correct ...
        x = self.UTILS.getElement(DOM.Calendar.mview_selected_day_title, "Selected day detail string")
        _expected_str = "%s %s %s %s" % (self._day_name, self._day_num, _now.month_name, _now.year)
        self.UTILS.TEST(_expected_str.lower() in x.text.lower(), 
                        "Day detail string: '%s' contains today's details ('%s')." % (x.text, _expected_str))
        
        x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Month view header")
        self.UTILS.TEST(_now.month_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (_now.month_name, x.text))
        
        self.UTILS.TEST(str(_now.year) in x.text,
                        "'%s' is in the header ('%s')." % (_now.year, x.text))
                
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot in month view with 'today' selected:", x)

    def _getNewDay(self, _now, _viewType):
        #
        # Private function to get a diffrent day (avoiding issues with month and week).
        #
        _days   = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        if _now.mday >= 25:
            self._day_num = _now.mday - 1
            if _now.wday == 0:
                self._day_name = _days[6]
            else:
                self._day_name = _days[_now.wday-1]

            self.UTILS.logResult("info", "<b>Testing <i>%s</i> view for <i>1 day in the past</i> ...</b>" % _viewType)
        else:
            self._day_num = _now.mday + 1
            if _now.wday > 6:
                self._day_name = _days[0]
            else:
                self._day_name = _days[_now.wday-1]

            self.UTILS.logResult("info", "<b>Testing <i>%s</i> view for <i>1 day in the future</i> ...</b>" % _viewType)

        self.calendar.setView("month")
        el_id_str = "d-%s-%s-%s" % (_now.year, _now.mon-1, self._day_num)
        x = self.UTILS.getElement( ("xpath", 
                                    "//li[@data-date='%s']" % el_id_str),
                                  "Cell for day %s/%s/%s" % (self._day_num, _now.mon, _now.year))
        x.tap()
        self.calendar.setView(_viewType)
