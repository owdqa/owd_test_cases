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
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Settings
from OWDTestToolkit.apps.browser import Browser



class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        self.Browser    = Browser(self)
        
        self.wifi_name  = self.UTILS.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user  = self.UTILS.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass  = self.UTILS.get_os_variable("GLOBAL_WIFI_PASSWORD")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Open the Settings application.
        #
        self.Settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)

        #
        # Return to this wifi and check the details.
        #
        self.Settings.wifi_list_tapName(self.wifi_name)

        self.UTILS.waitForElements(("xpath", "//h1[text()='%s']" % self.wifi_name), "Details for connected wifi - header", False)
        _forget = self.UTILS.getElement(DOM.Settings.wifi_details_forget_btn, "Details for connected wifi - forget button")
        _ip     = self.UTILS.getElement(DOM.Settings.wifi_details_ipaddress , "Details for connected wifi - ip address")
        _link   = self.UTILS.getElement(DOM.Settings.wifi_details_linkspeed , "Details for connected wifi - link speed")
        _sec    = self.UTILS.getElement(DOM.Settings.wifi_details_security  , "Details for connected wifi - security")
        _signal = self.UTILS.getElement(DOM.Settings.wifi_details_signal    , "Details for connected wifi - signal")

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot: ", x)
