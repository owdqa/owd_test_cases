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
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Settings


class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.Settings = Settings(self)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # WIFI.
        #
        self.UTILS.disableAllNetworkSettings()
        
        self.Settings.launch()
        self.UTILS.logResult("info", "<b>Check hotspot with DataConn and WiFi off.</b>")
        self.Settings.hotSpot()
        x = self.UTILS.getElement(DOM.Settings.hotspot_switch, "Hotspot switch")
        self.UTILS.TEST(not x.is_enabled(), "Hotspot switch is disabled.")
