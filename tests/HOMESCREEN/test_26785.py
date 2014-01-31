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
    
#     _RESTART_DEVICE = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        
        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        self.EME        = EverythingMe(self)

        self.UTILS.setPermission('Homescreen', 'geolocation', 'deny')
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):

        _appName = "Juegos Gratis"
        
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.getNetworkConnection()
        self.UTILS.switchToFrame(*DOM.Home.frame_locator)
        self.UTILS.uninstallApp(_appName)

        #
        # Launch the 'everything.me' app.
        #
        self.UTILS.logResult("info", "Launching EME ...")
        self.EME.launch()
        self.EME.bookmarkApp(_appName)

