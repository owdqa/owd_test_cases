#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#

class test_19414(GaiaTestCase):
    _Description = "[BASIC][BROWSER] Load a website via Wifi - verify the site loads in the browser correctly."
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Settings   = AppSettings(self)
        self.Browser    = AppBrowser(self)
        self.wifi_name  = self.UTILS.get_os_variable("GLOBAL_WIFI_NAME")
        self.testURL    = self.UTILS.get_os_variable("GLOBAL_TEST_URL")
        self.wifi_user  = self.UTILS.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass  = self.UTILS.get_os_variable("GLOBAL_WIFI_PASSWORD")

        
        self.data_layer.disable_wifi()
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Forget all networks (so we have to chose one).
        # Roy- *might* want this, but if we're already connected then this is a 'pass' anyway.
        #self.data_layer.forget_all_networks()
        
        #
        # Open the Settings application.
        #
        self.Settings.launch()
        
        #
        # Tap Wi-Fi.
        #
        self.Settings.wifi()

        #
        # Make sure wifi is set to 'on'.
        #
        self.Settings.turn_wifi_on()
        
        #
        # Connect to the wifi.
        #
        self.Settings.tap_wifi_network_name(self.wifi_name, self.wifi_user, self.wifi_pass)
        
        #
        # Tap specific wifi network (if it's not already connected).
        #
        self.UTILS.TEST(
                self.Settings.checkWifiLisetedAsConnected(self.wifi_name),
                "Wifi '" + self.wifi_name + "' is listed as 'connected' in wifi settings.", True)
            
        #
        # Open the browser app.
        #
        self.Browser.launch()
        
        #
        # Open our URL.
        #
        self.Browser.open_url(self.testURL)

        
        
        
        

