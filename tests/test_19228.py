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

class test_19228(GaiaTestCase):
    _Description = "(BLOCKED BY BUG 865232) [HOME SCREEN] Verify that when the user navigates to everything.me page, dock is hidden."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        
        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        self.EME        = EverythingMe(self)
        
        
        
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
        self.UTILS.switchToFrame(*DOM.Home.homescreen_iframe)
        self.UTILS.waitForElements(DOM.Home.dock, "Dock (before EME is opened)", True, 2, False)
                
        #
        # Launch the 'everything.me' app.
        #
        self.EME.launch()
        
        #
        # Verify that the dock is now hidden.
        #
        self.UTILS.waitForNotElements(DOM.Home.dock, "Dock (while EME is opened)", True, 20, False)
        
        
        
