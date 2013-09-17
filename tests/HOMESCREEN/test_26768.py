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
    
    _GROUP_NAME  = "Games"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        
        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        self.EME        = EverythingMe(self)
        
        #
        # Don't prompt me for geolocation (this was broken recently in Gaia, so 'try' it).
        #
        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        except:
            self.UTILS.logComment("(Just FYI) Unable to automatically set Homescreen geolocation permission.")

        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.getNetworkConnection()
         
        self.UTILS.switchToFrame(*DOM.Home.frame_locator)
        
        x = self.UTILS.getElements(DOM.Home.docked_apps, "Docked app icons", False)
        _boolOK = False
        for i in x:
            if "Browser" in i.get_attribute("aria-label"):
                _boolOK = True
                break
            
        self.UTILS.TEST(_boolOK, "Browser is in the dedicated dock icons.")
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot:", x)