#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)
        self.Browser   = Browser(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Data conn icon is not in status bar yet.
        #
        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("data") == False,
                         "Data mode is disabled before we start this test.")

        self.UTILS.statusbar.toggleViaStatusBar("data")

        #
        # Open the browser app. and check we can load a page.
        #
        self.Browser.launch()
        self.Browser.open_url("http://www.google.com")

        self.UTILS.statusbar.toggleViaStatusBar("data")

        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.element.waitForNotElements(DOM.Statusbar.dataConn, "Data icon in statusbar")

