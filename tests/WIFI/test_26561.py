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
import time


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
        # Return to this wifi and forget it.
        #
        self.Settings.wifi_list_tapName(self.wifi_name)
        self.Settings.wifi_forget()
        
        self.UTILS.TEST(self.Settings.wifi_list_isNotConnected(self.wifi_name), "%s is no longer connected" % self.wifi_name)
        
        #
        # make sure we need to add the details again.
        #
        self.Settings.wifi_list_tapName(self.wifi_name)
        time.sleep(1)
        self.UTILS.waitForElements(DOM.Settings.wifi_login_pass, "Password field")
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot after forgetting network: ", x)
