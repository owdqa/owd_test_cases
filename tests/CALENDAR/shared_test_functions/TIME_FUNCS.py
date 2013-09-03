#
# Some functions that are shard between tests (26685 and 26686 for example).
#

#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from marionette import Marionette
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *
#
# Imports particular to this test case.
#
import os, time

class main(GaiaTestCase):

    def _getNewDay(self, p_numDays, p_viewType):
        #
        # Changes the calendar day to a different day relative to 'today' - uses the
        # month view to do this, then switches back to whichever
        # view you want (month, week, day).<br>
        # Returns an array:<br>
        # 0 = day number (0-31).
        # 1 = day of week name.
        #
        self.actions    = Actions(self.marionette)
        
        _days      = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        _month_end = [31,28,31,30,31,30,31,31,30,31,30,31]
        _now_secs  = time.time()
        _now_diff  = int(_now_secs) + (86400*p_numDays)
        _today     = self.UTILS.getDateTimeFromEpochSecs(_now_secs)
        _new_today = self.UTILS.getDateTimeFromEpochSecs(_now_diff)
                    
        #
        # Switch to month view and tap this day, then switch back to our view.
        #
        self.calendar.setView("month")
        
        mon_diff = (_today.mon - _new_today.mon)
        self.UTILS.logResult("info", "x: %s" % mon_diff)
        if mon_diff > 0:
            el = 0
            y2 = 500
        if mon_diff < 0:
            el = 6
            y2 = -500
            mon_diff = mon_diff * -1
            
        for i in range (0,mon_diff):
            # go left (by flicking right)
            x = self.UTILS.getElements(DOM.Calendar.mview_first_row_for_flick, "First row of dates (for scrolling)")[el]
            self.actions.flick(x,0,0,y2,0).perform()

            
        
        el_id_str = "d-%s-%s-%s" % (_new_today.year, _new_today.mon-1, _new_today.mday)
        x = self.UTILS.getElement( ("xpath", 
                                    "//li[@data-date='%s']" % el_id_str),
                                  "Cell for day %s/%s/%s" % (_new_today.mday, _new_today.mon, _new_today.year))
        x.tap()
        self.calendar.setView(p_viewType)

        
        return _new_today