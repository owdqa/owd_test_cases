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
        self.settings.launch()
        
        self.settings.wifi()
   
        self.settings.wifi_switchOn()
           
        self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
           
        self.UTILS.TEST(self.UTILS.isNetworkTypeEnabled("wifi") == True, "Wifi mode is now enabled.")
