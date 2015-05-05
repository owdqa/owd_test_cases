# 26463: Status bar- Radio: Airplane mode icon
# ** Procedure
#       1- Turn the device on with a valid SIM Card
#       2- Wait until it is attached to the network-
#       3- Turn bluetooth and data connection on
#       3- Go to Settings and turn Airplane mode on
#       4- Verify that an icon appears on the status bar
#       5- Also, verify that the radio icons dissapear (signal, bluetooth, data connection)
# ** Expected Results
#       When Airplane mode is activated it appears an icon on the status bar.
#       All radio icons that could be on the status bar, dissapear since
#       activating Airplane mode should deactivate all radio functionalities

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS


class test_main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)

    def tearDown(self):
        self.data_layer.set_setting('ril.radio.disabled', False)
        self.wait_for_condition(lambda m: not self.data_layer.get_setting(
            'ril.radio.disabled'), timeout=20, message="Device attached to a mobile network")
        self.UTILS.test.test(not self.data_layer.get_setting('ril.radio.disabled'), "Radio comms is again enabled.")

        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        if self.data_layer.get_setting('ril.radio.disabled'):
            # enable the device radio, disable Airplane mode
            self.data_layer.set_setting('ril.radio.disabled', False)
            self.wait_for_condition(lambda m: not self.data_layer.get_setting(
                'ril.radio.disabled'), timeout=20, message="Device attached to a mobile network")

        self.marionette.switch_to_frame()
        self.UTILS.element.waitForElements(DOM.Statusbar.signal_connected, "Signal icon in statusbar", True, 5, False)

        self.data_layer.bluetooth_enable()
        self.wait_for_condition(lambda m: self.data_layer.bluetooth_is_enabled,
                                timeout=20, message="Bluetooth enabled")
        self.UTILS.element.waitForElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar", True, 5, False)

        self.data_layer.connect_to_cell_data()
        self.wait_for_condition(lambda m: self.data_layer.is_cell_data_connected,
                                timeout=20, message="Device attached to data connection")
        self.UTILS.element.waitForElements(DOM.Statusbar.dataConn, "Data conn icon in statusbar", True, 5, False)

        self.UTILS.statusbar.toggleViaStatusBar("airplane")
        self.UTILS.test.test(self.data_layer.get_setting('ril.radio.disabled'), "Radio comms is now disabled.")

        # Visual checking
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForElements(DOM.Statusbar.airplane, "Airplane icon in statusbar", True, 5, False)
        self.UTILS.element.waitForNotElements(
            DOM.Statusbar.signal_connected, "Signal icon in statusbar", True, 5, False)
        self.UTILS.element.waitForNotElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar", True, 5, False)
        self.UTILS.element.waitForNotElements(DOM.Statusbar.dataConn, "Data conn icon in statusbar", True, 5, False)
