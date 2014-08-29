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
        # Open the Settings application.
        #
        self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)

        #
        # Return to this wifi and check the details.
        #
        self.settings.wifi_list_tapName(self.wifi_name)

        self.UTILS.element.waitForElements(("xpath", "//h1[text()='%s']" % self.wifi_name), "Details for connected wifi - header", False)
        _forget = self.UTILS.element.getElement(DOM.Settings.wifi_details_forget_btn, "Details for connected wifi - forget button")
        _ip = self.UTILS.element.getElement(DOM.Settings.wifi_details_ipaddress , "Details for connected wifi - ip address")
        _link = self.UTILS.element.getElement(DOM.Settings.wifi_details_linkspeed , "Details for connected wifi - link speed")
        _sec = self.UTILS.element.getElement(DOM.Settings.wifi_details_security  , "Details for connected wifi - security")
        _signal = self.UTILS.element.getElement(DOM.Settings.wifi_details_signal    , "Details for connected wifi - signal")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot: ", x)
