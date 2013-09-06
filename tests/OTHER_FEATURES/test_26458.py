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

class test_main(GaiaTestCase):

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
        self.data_layer.bluetooth_disable()
        
        self.UTILS.waitForNotElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar")
        self.UTILS.TEST(self.UTILS.isNetworkTypeEnabled("bluetooth") == False,
                         "Bluetooth is disabled before we start this test.")

        #
        # Enable airplane mode.
        #
        self.UTILS.toggleViaStatusBar("bluetooth")
        
        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.waitForElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar", True, 20, False)
        
        #
        # Disable airplane mode.
        #
        self.UTILS.toggleViaStatusBar("bluetooth")
        
        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.waitForNotElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar")
        
