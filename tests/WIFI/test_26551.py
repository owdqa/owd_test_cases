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
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.browser import Browser


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.Settings = Settings(self)
        self.Browser = Browser(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Open the Settings application.
        #
        self.UTILS.network.getNetworkConnection()

        #
        # Open the browser app.
        #
        self.Browser.launch()

        #
        # Open our URL.
        #
        self.Browser.open_url("www.google.com")
        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)

        self.Browser.open_url("www.wikipedia.com")
        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)
