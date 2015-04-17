from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.calendar import Calendar


class test_main(PixiTestCase):

    day_num = 0
    day_name = ""

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.calendar = Calendar(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

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
