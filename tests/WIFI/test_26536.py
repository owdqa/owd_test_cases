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
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        
        self.wifi_name  = self.UTILS.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user  = self.UTILS.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass  = self.UTILS.get_os_variable("GLOBAL_WIFI_PASSWORD")

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # WIFI.
        #
        self.Settings.launch()
    
        self.Settings.wifi()
        self.Settings.turn_wifi_on()
        self.Settings.tap_wifi_network_name(self.wifi_name, self.wifi_user, self.wifi_pass)
        
        x = self.Settings.goBack()
           
        #
        # Tap hotspot.
        #
        self.UTILS.logResult("info", "<b>Check hotspot with WIFI on.</b>")
        self.Settings.enable_hotSpot()

        self.Settings.disable_hotSpot()
        self.UTILS.disableAllNetworkSettings()
        self.UTILS.toggleViaStatusBar("data")
        
        self.Settings.launch()
        self.UTILS.logResult("info", "<b>Check hotspot with DataConn on.</b>")
        self.Settings.enable_hotSpot()
