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


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.Settings = Settings(self)

        self.wifi_name  = self.UTILS.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user  = self.UTILS.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass  = self.UTILS.get_os_variable("GLOBAL_WIFI_PASSWORD")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Data conn icon is not in status bar yet.
        #
        self.data_layer.disable_wifi()
        
        self.UTILS.waitForNotElements(DOM.Statusbar.wifi, "Wifi icon in statusbar")
        self.UTILS.TEST(self.UTILS.isNetworkTypeEnabled("wifi") == False,
                         "Wifi is disabled before we start this test.")

        #
        # Enable wifi mode.
        #
        self.UTILS.toggleViaStatusBar("wifi")
        
        #
        # If required, connect to the wifi.
        #
        self.marionette.switch_to_frame()
        try:
            self.wait_for_element_present("xpath", "//iframe[contains(@%s,'%s')]" %\
                                           (DOM.Settings.frame_locator[0], DOM.Settings.frame_locator[1]),
                                           timeout=5)
            
            #
            # We need to supply the login details for the network.
            #
            self.UTILS.switchToFrame(*DOM.Settings.frame_locator)
            self.Settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
               
            self.marionette.switch_to_frame()
        except:
            pass

        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.waitForElements(DOM.Statusbar.wifi, "Wifi icon in statusbar", True, 20, False)
        
        #
        # Disable wifi mode.
        #
        self.UTILS.toggleViaStatusBar("wifi")
        
        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.waitForNotElements(DOM.Statusbar.wifi, "Wifi icon in statusbar")
        
