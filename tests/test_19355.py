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
import time

class test_19355(GaiaTestCase):
    _Description = "[UTILITY TRAY] Activate/Deactivate ariplane mode from Utility tray icon."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Data conn icon is not in status bar yet.
        #
        self.UTILS.TEST(self.UTILS.isNetworkTypeEnabled("airplane") == False,
                         "Airplane mode is disabled before we start this test.")
        
        #
        # Enable airplane mode.
        #
        self.UTILS.toggleViaStatusBar("airplane")
        
        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.waitForElements(DOM.Statusbar.airplane, "Airplane icon in statusbar", True, 20, False)
        
        #
        # Disable airplane mode.
        #
        self.UTILS.toggleViaStatusBar("airplane")
        
        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.waitForNotElements(DOM.Statusbar.airplane, "Airplane icon in statusbar")
        
