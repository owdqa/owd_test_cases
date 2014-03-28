#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.Browser = Browser(self)
        self.testURL = self.UTILS.general.get_os_variable("GLOBAL_TEST_URL")
        self.UTILS.reporting.logComment("Using " + self.testURL)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Wifi needs to be off for this test to work.
        #
        self.UTILS.statusbar.toggleViaStatusBar("data")

        #
        # Open the browser app.
        #
        self.Browser.launch()

        #
        # Open our URL.
        #
        self.Browser.open_url(self.testURL)

        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)

        x = self.UTILS.element.getElement(DOM.Browser.tab_tray_open, "Tab tray icon")
        x.tap()

        self.UTILS.element.waitForElements(DOM.Browser.tab_tray_screen, "Tab screen")

        x = self.UTILS.element.getElement(DOM.Browser.settings_button, "Settings icon")
        x.tap()

        self.UTILS.element.waitForElements(DOM.Browser.settings_header, "Settings header")
