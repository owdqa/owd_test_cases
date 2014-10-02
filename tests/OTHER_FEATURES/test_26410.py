# OWD-26410: As a user, I want to be able to enable/disable Bluetooth from the utility tray
# ** Procedure
#       1- Open Utility Tray
#       2- Press on the Bluetooth icon to Enable it(ER1)
#       3- Open Settings app to verify that bluetooth is working
#       4- Open utility tray again
#       5- Now disable the bluetooth icon (ER2)
#
# ** Expected Results
#       (ER1)When enabling bluetooth, its icon is shown on the status bar
#       (ER2) The bluetooth icon dissapears when disconnected

import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from tests.i18nsetup import setup_translations
from gaiatest import GaiaData
from gaiatest import GaiaApps


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        _ = setup_translations(self)

        # Make sure bluetooth is not enabled before the tests starts
        self.data_layer.bluetooth_disable()
        self.wait_for_condition(lambda m: not self.data_layer.bluetooth_is_enabled,
                                timeout=20, message="Bluetooth disabled")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.toggleViaStatusBar("bluetooth")
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar", True, 20, False)

        # Open settings and check bluetooth is on.
        self.settings.launch()

        bluetooth = self.UTILS.element.getElement(DOM.Settings.bluetooth, "Bluetooth")
        self.UTILS.element.scroll_into_view(bluetooth)
        time.sleep(3)

        bluetooth_description = self.UTILS.element.getElement(DOM.Settings.bluetooth_desc, "Bluetooth description")
        self.UTILS.test.TEST(bluetooth_description.text == _("No devices paired"), "Bluetooth is marked as turned on.")

        self.UTILS.statusbar.toggleViaStatusBar("bluetooth")
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(DOM.Statusbar.bluetooth, "Bluetooth icon in statusbar")
