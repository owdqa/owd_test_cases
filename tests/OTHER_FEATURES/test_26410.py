#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        
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
        # Enable bluetooth mode.
        #
        self.UTILS.toggleViaStatusBar("bluetooth")
        
        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.waitForElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar", True, 20, False)
        
        #
        # Open settings and check bluetooth is on.
        #
        self.settings.launch()
        
        x = self.UTILS.getElement(DOM.Settings.bluetooth_desc, "Bluetooth description")
        self.UTILS.TEST(x.text == "No devices paired", "Bluetooth is marked as turned on.")
                
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot:", x)
        
        #
        # Disable bluetooth mode.
        #
        self.UTILS.toggleViaStatusBar("bluetooth")
        
        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.waitForNotElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar")
        
