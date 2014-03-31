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
from OWDTestToolkit.utils.utils import UTILS
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
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Data conn icon is not in status bar yet.
        #
        self.data_layer.bluetooth_disable()

        self.UTILS.element.waitForNotElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar")
        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("bluetooth") == False,
                         "Bluetooth is disabled before we start this test.")

        #
        # Enable bluetooth mode.
        #
        self.UTILS.statusbar.toggleViaStatusBar("bluetooth")

        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.element.waitForElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar", True, 20, False)

        #
        # Open settings and check bluetooth is on.
        #
        self.settings.launch()

        x = self.UTILS.element.getElement(DOM.Settings.bluetooth_desc, "Bluetooth description")
        self.UTILS.test.TEST(x.text == "No devices paired", "Bluetooth is marked as turned on.")
    
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot:", x)

        #
        # Disable bluetooth mode.
        #
        self.UTILS.statusbar.toggleViaStatusBar("bluetooth")

        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.element.waitForNotElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar")

