#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.browser import Browser

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
        self.Browser = Browser(self)
        self.testURL = self.UTILS.get_os_variable("GLOBAL_TEST_URL")

        self.UTILS.logComment("Using " + self.testURL)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Wifi needs to be off for this test to work.
        #
        self.UTILS.toggleViaStatusBar("data")

        #
        # Open the browser app.
        #
        self.Browser.launch()

        #
        # Open our URL.
        #
        self.Browser.open_url(self.testURL)
