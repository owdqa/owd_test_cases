from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS



class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Data conn icon is not in status bar yet.
        #
        self.data_layer.bluetooth_disable()

        self.UTILS.element.waitForNotElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar")
        self.UTILS.test.test(self.UTILS.network.is_network_type_enabled("bluetooth") == False,
                         "Bluetooth is disabled before we start this test.")

        #
        # Enable airplane mode.
        #
        self.UTILS.statusbar.toggleViaStatusBar("bluetooth")

        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.element.waitForElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar", True, 20, False)

        #
        # Disable airplane mode.
        #
        self.UTILS.statusbar.toggleViaStatusBar("bluetooth")

        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.element.waitForNotElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar")

