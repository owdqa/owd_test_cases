#===============================================================================
# 26561: Forget this network option
#
# Pre-requisites:
# To have at least one known network
#
# Procedure:
# 1- On the device under test turn Wi-Fi on
# 2- Search and connect to a Wi-Fi network
# 3- Once the connection has been done correctly, and the networks
# appears as connected, tap on its name so the details dialog is open
# 4- There, go to "Forget this network" option and click on it
# 5- Verify that the network does not appear as known anymore
#
# Expected results:
# There should be possible to remove a network from the known ones by
# using the option given for that.
# The device is able to remove the network from the known ones.
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.browser import Browser


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.Browser = Browser(self)

        self.wifi_name = self.UTILS.general.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user = self.UTILS.general.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass = self.UTILS.general.get_os_variable("GLOBAL_WIFI_PASSWORD")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.settings.launch()
        self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
        network = {'ssid': self.wifi_name}
        self.wait_for_condition(lambda m: self.data_layer.is_wifi_connected(network), timeout=30)

        self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)
        self.settings.wifi_list_tapName(self.wifi_name)
        self.settings.wifi_forget()

        self.UTILS.test.TEST(not self.data_layer.is_wifi_connected(),
                             "{} is no longer connected".format(self.wifi_name))

        #
        # make sure we need to add the details again.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)
        self.settings.wifi_list_tapName(self.wifi_name)
        time.sleep(1)
        self.UTILS.element.waitForElements(DOM.Settings.wifi_login_pass, "Password field")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot after forgetting network: ", x)
