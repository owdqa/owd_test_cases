#===============================================================================
# 26550: Connectivity icon
#
# Procedure:
# 1- On the device, turn Wi-Fi on
# 2- Verify if the handset shows an icon indicating that the Wi-Fi connection
# is activated
# 3- Finish the Wi-Fi connection. Verify the icon disappears from the display
#
# Expected results:
# There should be an icon on the screen or something to inform user if he is
# connected to a Wi-Fi or not. When user is connected, the icon indicating the
# Wi-Fi connection must appear of the display. When user disconnects the Wi-Fi,
# the icon indicating the Wi-Fi connection must disappear of the display.
#===============================================================================

from gaiatest import GaiaTestCase
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

        self.wifi_name = self.UTILS.general.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_pass = self.UTILS.general.get_os_variable("GLOBAL_WIFI_PASSWORD")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Data conn icon is not in status bar yet.
        #
        self.data_layer.disable_wifi()

        self.UTILS.element.waitForNotElements(DOM.Statusbar.wifi, "Wifi icon in statusbar")
        self.UTILS.test.TEST(self.UTILS.network.is_network_type_enabled("wifi") == False,
                         "Wifi is disabled before we start this test.")

        self.settings.launch()
        self.settings.wifi()
        self.settings.connect_to_wifi(self.wifi_name, self.wifi_pass)

        self.marionette.switch_to_frame()
        self.UTILS.element.waitForElements(DOM.Statusbar.wifi, "Wifi icon in statusbar", True, 20, False)

        #
        # Disable wifi mode.
        #
        self.UTILS.home.goHome()
        self.settings.launch()
        self.settings.wifi()
        self.settings.wifi_switchOff()

        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.element.waitForNotElements(DOM.Statusbar.wifi, "Wifi icon not in statusbar")
