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
    
    _offset_days    = 1
    
    def setUp(self):
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
        
        _today = self.UTILS.getDateTimeFromEpochSecs(int(time.time()))
        
        #===================================================================================================
        #
        # MONTH view
        #
        self.calendar.setView("month")
          
        self.UTILS.logResult("info", "<b>Testing <u>month</u> view for <i>today</i> ...</b>")
        self.calendar.setView("today")
        self._monthViewTests(_today)
          
        self.UTILS.logResult("info", "<b>Testing <u>month</u> view for <i>%s days ago</i> ...</b>" % self._offset_days)
        x = self.calendar.changeDay(self._offset_days, "month")
        self._monthViewTests(x)
 
        #===================================================================================================
        #
        # WEEK view
        #
        self.calendar.setView("week")
         
        self.UTILS.logResult("info", "<b>Testing <i>week</i> view for <i>today</i> ...</b>")
        self.calendar.setView("today")
        self._weekViewTests(_today)
          
        self.UTILS.logResult("info", "<b>Testing <u>week</u> view for <i>%s days ago</i> ...</b>" % self._offset_days)
        x = self.calendar.changeDay(self._offset_days, "week")
        self._weekViewTests(x)

        #===================================================================================================
        #
        # DAY view
        #
        self.calendar.setView("day")
        
        self.UTILS.logResult("info", "<b>Testing <i>day</i> view for <i>today</i> ...</b>")
        self.calendar.setView("today")
        self._dayViewTests(_today)
         
        self.UTILS.logResult("info", "<b>Testing <u>day</u> view for <i>%s days ago</i> ...</b>" % self._offset_days)
        x = self.calendar.changeDay(self._offset_days, "day")
        self._dayViewTests(x)



    def _dayViewTests(self, p_now):
        x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Day view header")

        self.UTILS.TEST(p_now.day_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (p_now.day_name, x.text))
        
        self.UTILS.TEST(p_now.month_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (p_now.day_name, x.text))
        
        self.UTILS.TEST(str(p_now.mday) in x.text,
                        "'%s' is in the header ('%s')." % (p_now.mday, x.text))
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot in day view with 'today' selected:", x)
        
        
    def _weekViewTests(self, p_now):
        x        = self.UTILS.getElement(DOM.Calendar.wview_active_days, "Active days")
        _testStr = "%s %s" % (p_now.day_name[:3].upper(), p_now.mday)
        
        self.UTILS.TEST(_testStr in x.text.upper(), 
                        "Selected day ('%s') is one of the displayed days: '%s'" % (_testStr, x.text.replace('\n',', ')))
        
        x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Week view header")
        self.UTILS.TEST(p_now.month_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (p_now.month_name, x.text))
        
        self.UTILS.TEST(str(p_now.year) in x.text,
                        "'%s' is in the header ('%s')." % (p_now.year, x.text))
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot in week view with 'today' selected:", x)
        
        
    def _monthViewTests(self, p_now):
        # Highlighted cell is correct ...
        el_id_str = "d-%s-%s-%s" % (p_now.year, p_now.mon-1, p_now.mday)
        self.UTILS.waitForElements( ("xpath", 
                                    "//li[@data-date='%s' and contains(@class, 'selected')]" % el_id_str),
                                  "Selected day for %s/%s/%s" % (p_now.mday, p_now.mon, p_now.year), True, 2, False)

        # Selected day string is correct ...
        x = self.UTILS.getElement(DOM.Calendar.mview_selected_day_title, "Selected day detail string")
        _expected_str = "%s %s %s %s" % (p_now.day_name, p_now.mday, p_now.month_name, p_now.year)
        self.UTILS.TEST(_expected_str.lower() in x.text.lower(), 
                        "Day detail string: '%s' contains today's details ('%s')." % (x.text, _expected_str))
        
        x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Month view header")
        self.UTILS.TEST(p_now.month_name.lower() in x.text.lower(),
                        "'%s' is in the header ('%s')." % (p_now.month_name, x.text))
        
        self.UTILS.TEST(str(p_now.year) in x.text,
                        "'%s' is in the header ('%s')." % (p_now.year, x.text))
                
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot in month view with 'today' selected:", x)


