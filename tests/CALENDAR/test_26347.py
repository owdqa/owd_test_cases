from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.calendar import Calendar
from OWDTestToolkit.apps.settings import Settings

from datetime import datetime


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.calendar = Calendar(self)
        self.settings = Settings(self)
        self.titleStr = "Test event " + str(datetime.now().time())
        self.locatStr = "Right here"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch contacts app.
        self.calendar.launch()

        self.calendar.createEvent()

        self.UTILS.reporting.logResult(False, "NOTE FOR ROY: need to check this event in each view (see jira for details).")
