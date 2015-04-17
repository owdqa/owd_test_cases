from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.browser = Browser(self)
        self.testURL = self.UTILS.general.get_config_variable("test_url", "common")
        self.UTILS.reporting.logComment("Using " + self.testURL)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Wifi needs to be off for this test to work.
        #
        self.data_layer.connect_to_cell_data()

        #
        # Open the browser app.
        #
        self.browser.launch()

        #
        # Open our URL.
        #
        self.browser.open_url(self.testURL)

        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)

        x = self.UTILS.element.getElement(DOM.Browser.tab_tray_open, "Tab tray icon")
        x.tap()

        self.UTILS.element.waitForElements(DOM.Browser.tab_tray_screen, "Tab screen", True, 2, False)

        x = self.UTILS.element.getElement(DOM.Browser.tab_tray_new_tab_btn, "New tab icon")
        x.tap()

        self.UTILS.element.waitForNotElements(DOM.Browser.tab_tray_screen, "Tab screen", True, 2, False)
        self.UTILS.element.waitForElements(DOM.Browser.new_tab_screen, "New tab")
