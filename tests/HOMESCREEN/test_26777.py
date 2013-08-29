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
        self.Settings   = Settings(self)
        self.EME        = EverythingMe(self)

        self.UTILS.setPermission('Homescreen', 'geolocation', 'deny')
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.getNetworkConnection()

        #
        # Veriy that the dock is displayed.
        #
        self.UTILS.switchToFrame(*DOM.Home.frame_locator)
        self.UTILS.waitForElements(DOM.Home.dock, "Dock (before EME is opened)", True, 2, False)
                
        #
        # Launch the 'everything.me' app.
        #
        self.UTILS.logResult("info", "Launching EME ...")
        self.EME.launch()
        
        #
        # Close EME.
        #
        self.UTILS.logResult("info", "Closing EME ...")
        self.UTILS.scrollHomescreenRight()
        
        #
        # Verify that the dock is now visible again.
        #
        self.UTILS.waitForElements(DOM.Home.dock, "Dock (after EME is closed)", True, 2, False)
        
