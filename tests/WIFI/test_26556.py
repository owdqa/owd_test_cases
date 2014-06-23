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
import time


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.browser = Browser(self)

        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Open the browser app.
        #
        self.browser.launch()
        self.browser.open_url("www.google.com")

        self.lockscreen.lock()

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Srceenshot of locked screen:", x)

        time.sleep(3)
        self.lockscreen.unlock()

        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)

        self.browser.open_url("www.wikipedia.com")
