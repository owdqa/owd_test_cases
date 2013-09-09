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

class test_main(GaiaTestCase):

    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.settings   = Settings(self)

        self.wifi_name  = self.UTILS.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user  = self.UTILS.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass  = self.UTILS.get_os_variable("GLOBAL_WIFI_PASSWORD")
        
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        self.UTILS.TEST(self.UTILS.isNetworkTypeEnabled("wifi") == False, "Wifi is disabled.")
        
        self.settings.launch()
        
        self.settings.wifi()
   
        self.settings.turn_wifi_on()
           
        self.settings.tap_wifi_network_name(self.wifi_name, self.wifi_user, self.wifi_pass)
           
        self.UTILS.TEST(
                self.settings.checkWifiConnected(self.wifi_name),
                "Wifi '" + self.wifi_name + "' is listed as 'connected' in wifi settings.", True)
        
        self.UTILS.TEST(self.UTILS.isNetworkTypeEnabled("wifi") == True, "Wifi mode is now enabled.")
