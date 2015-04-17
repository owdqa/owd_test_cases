from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.browser import Browser


class test_main(PixiTestCase):

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.Browser = Browser(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Open the Settings application.
        #
        self.connect_to_network()

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
