#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

        self.wifi_name = self.UTILS.general.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user = self.UTILS.general.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass = self.UTILS.general.get_os_variable("GLOBAL_WIFI_PASSWORD")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # WIFI.
        #
        self.settings.launch()

        self.settings.wifi()
        self.settings.wifi_switchOn()
        self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)

        self.settings.goBack()

        #
        # Tap hotspot.
        #
        self.settings.hotSpot()

        self.UTILS.reporting.logResult("info", "<b>Check hotspot with WIFI on.</b>")
        self.settings.enable_hotSpot()

        self.settings.disable_hotSpot()
        self.UTILS.network.disableAllNetworkSettings()
        self.UTILS.statusbar.toggleViaStatusBar("data")

        self.settings.launch()
        self.UTILS.reporting.logResult("info", "<b>Check hotspot with DataConn on.</b>")
        self.settings.enable_hotSpot()
