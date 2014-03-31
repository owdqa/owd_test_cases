#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
import time
from OWDTestToolkit import DOM
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.calendar import Calendar

#
# Imports particular to this test case.
#


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.calendar = Calendar(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        now = self.UTILS.date_and_time.getDateTimeFromEpochSecs(int(time.time()))

        #
        # Launch contacts app.
        #
        self.calendar.launch()

        self.calendar.setView("month")
        self.calendar.setView("today")

        #
        # Check month view details are correct for 'today'.
        #
        x = self.UTILS.element.getElement(DOM.Calendar.current_view_header, "Header")
        expected_str = "{} {}".format(now.month_name, now.year)
        self.UTILS.test.TEST(expected_str.lower() in x.text.lower(),
                        "Header: '{}' contains today's details ('{}').".format(x.text, expected_str))

        x = self.UTILS.element.getElement(DOM.Calendar.mview_selected_day_title, "Selected day detail string")
        expected_str = "{}".format(now.mday)
        self.UTILS.test.TEST(expected_str.lower() in x.text.lower(),
                        "Day detail string: '{}' contains today's details ('{}').".format(x.text, expected_str))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point:", x)
