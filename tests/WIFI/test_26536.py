#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Settings


class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
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
        # WIFI.
        #
        self.Settings.launch()
    
        self.Settings.wifi()
        self.Settings.wifi_switchOn()
        self.Settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
        
        self.Settings.goBack()
           
        #
        # Tap hotspot.
        #

        self.Settings.hotSpot()

        self.UTILS.logResult("info", "<b>Check hotspot with WIFI on.</b>")
        self.Settings.enable_hotSpot()

        self.Settings.disable_hotSpot()
        self.UTILS.disableAllNetworkSettings()
        self.UTILS.toggleViaStatusBar("data")
        
        self.Settings.launch()
        self.UTILS.logResult("info", "<b>Check hotspot with DataConn on.</b>")
        self.Settings.enable_hotSpot()
