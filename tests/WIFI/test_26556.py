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
import time


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.Browser = Browser(self)

        self.wifi_name = self.UTILS.general.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user = self.UTILS.general.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass = self.UTILS.general.get_os_variable("GLOBAL_WIFI_PASSWORD")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Open the settings application.
        #
        self.settings.launch()
        self.settings.wifi()
        self.settings.wifi_switchOn()
        self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)

        #
        # Open the browser app.
        #
        self.Browser.launch()
        self.Browser.open_url("www.google.com")

        self.lockscreen.lock()

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Srceenshot of locked screen:", x)

        time.sleep(3)
        self.lockscreen.unlock()

        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)

        self.Browser.open_url("www.wikipedia.com")
