#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.browser import Browser


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

        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)

        x = self.UTILS.getElement(DOM.Browser.tab_tray_open, "Tab tray icon")
        x.tap()

        self.UTILS.waitForElements(DOM.Browser.tab_tray_screen, "Tab screen", True, 2, False)

        x = self.UTILS.getElement(DOM.Browser.tab_tray_new_tab_btn, "New tab icon")
        x.tap()

        self.UTILS.waitForNotElements(DOM.Browser.tab_tray_screen, "Tab screen", True, 2, False)
        self.UTILS.waitForElements(DOM.Browser.new_tab_screen, "New tab")
