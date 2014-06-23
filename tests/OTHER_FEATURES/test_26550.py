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

        self.wifi_name = self.UTILS.general.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user = self.UTILS.general.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass = self.UTILS.general.get_os_variable("GLOBAL_WIFI_PASSWORD")

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Data conn icon is not in status bar yet.
        #
        self.data_layer.disable_wifi()

        self.UTILS.element.waitForNotElements(DOM.Statusbar.wifi, "Wifi icon in statusbar")
        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("wifi") == False,
                         "Wifi is disabled before we start this test.")

        #
        # Enable wifi mode.
        #
        self.data_layer.connect_to_wifi()

        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.element.waitForElements(DOM.Statusbar.wifi, "Wifi icon in statusbar", True, 20, False)

        #
        # Disable wifi mode.
        #
        self.data_layer.disable_wifi()
        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.element.waitForNotElements(DOM.Statusbar.wifi, "Wifi icon not in statusbar")
