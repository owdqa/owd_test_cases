#===============================================================================
# 26412: As a user, I want to be able to enable/disable WiFi from the
# utility tray
#
# Procedure:
# 1- Open Utility Tray
# 2- Press on the wifi icon to Enable it(ER1)
# 3- Connect to a wifi network
# 4- Open utility tray again
# 5- Now disable the wifi icon (ER2)
#
# Expected results:
# (ER1)When enabling it user is redirected to the settings app so that
# he can select the WiFi to be connected to.
# When connected to a wifi the icon is shown
# (ER2) The wifi icon dissappears when disconnected
#===============================================================================

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(SpreadtrumTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

        self.wifi_name = self.UTILS.general.get_config_variable("ssid", "wifi")
        self.wifi_pass = self.UTILS.general.get_config_variable("password", "wifi")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.disable_wifi()
        self.UTILS.element.waitForNotElements(DOM.Statusbar.wifi, "Wifi icon in statusbar")
        self.UTILS.test.test(not self.UTILS.network.is_network_type_enabled("wifi"),
                         "Wifi is disabled before we start this test.")

        self.UTILS.statusbar.toggleViaStatusBar("wifi")
        # If required, connect to the wifi.
        self.marionette.switch_to_frame()
        try:
            self.wait_for_element_present("xpath", "//iframe[contains(@{},'{}')]".\
                                        format(DOM.Settings.frame_locator[0], DOM.Settings.frame_locator[1]),
                                        timeout=10)

            # We need to supply the login details for the network.
            self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)
            self.settings.connect_to_wifi(self.wifi_name, self.wifi_pass)
            self.marionette.switch_to_frame()
        except:
            pass

        self.UTILS.element.waitForElements(DOM.Statusbar.wifi, "Wifi icon in statusbar", timeout=20)
        self.UTILS.statusbar.toggleViaStatusBar("wifi")
        self.UTILS.element.waitForNotElements(DOM.Statusbar.wifi, "Wifi icon in statusbar", timeout=20)
