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
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        if self.data_layer.get_setting('ril.radio.disabled'):
            # enable the device radio, disable Airplane mode
            self.data_layer.set_setting('ril.radio.disabled', False)
            time.sleep(1)

        self.UTILS.element.waitForElements(DOM.Statusbar.signal, "Signal icon in statusbar", True, 5, False)

        self.data_layer.bluetooth_enable()
        self.UTILS.element.waitForElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar", True, 5, False)

        self.data_layer.connect_to_cell_data()
        self.UTILS.element.waitForElements(DOM.Statusbar.dataConn, "Data conn icon in statusbar", True, 5, False)

        #
        # Enable airplane mode.
        #
        self.UTILS.statusbar.toggleViaStatusBar("airplane")

        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.element.waitForElements(   DOM.Statusbar.airplane , "Airplane icon in statusbar" , True, 5, False)
        self.UTILS.element.waitForNotElements(DOM.Statusbar.signal   , "Signal icon in statusbar"   , True, 5, False)
        self.UTILS.element.waitForNotElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar", True, 5, False)
        self.UTILS.element.waitForNotElements(DOM.Statusbar.dataConn , "Data conn icon in statusbar", True, 5, False)

        #
        # Disable airplane mode.
        #
        self.UTILS.test.TEST(self.data_layer.get_setting('ril.radio.disabled'), "Radio comms is now disabled.")