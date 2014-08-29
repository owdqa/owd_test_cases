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
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # WIFI.
        #
        self.UTILS.network.disableAllNetworkSettings()

        self.settings.launch()
        self.UTILS.reporting.logResult("info", "<b>Check hotspot with DataConn and WiFi off.</b>")
        self.settings.hotSpot()
        x = self.UTILS.element.getElement(DOM.Settings.hotspot_switch, "Hotspot switch")
        self.UTILS.test.TEST(not x.is_enabled(), "Hotspot switch is disabled.")
