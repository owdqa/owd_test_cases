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
        self.Settings.launch()
        self.Settings.wifi()
        self.Settings.wifi_switchOn()
        self.Settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
                        
        #
        # Open the browser app.
        #
        self.Browser.launch()
        self.Browser.open_url("www.google.com")

        self.lockscreen.lock()
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Srceenshot of locked screen:", x)
        
        time.sleep(3)
        self.lockscreen.unlock()
        
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        
        self.Browser.open_url("www.wikipedia.com")
        

