#===============================================================================
# 26536: Verify that it is possible to turn Wi-Fi HotSpot on/off
# using the dedicated icon when the device has data on or it is
# connected to a Wi-Fi network
#
# Procedure:
# Verify that it is possible to enable/disable this option
#
# Expected results:
# The HotSpot can be turned on and off
#===============================================================================
import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(FireCTestCase):

    def setUp(self):
        # Set up child objects...
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()
        self.settings.launch()

        #
        # Tap hotspot.
        #
        self.settings.hotSpot()

        self.UTILS.reporting.logResult("info", "<b>Check hotspot with WIFI on.</b>")
        self.settings.enable_hotSpot()

        time.sleep(3)
        self.settings.disable_hotSpot()
        self.UTILS.network.disableAllNetworkSettings()

        self.data_layer.connect_to_cell_data()
        self.settings.launch()
        self.UTILS.reporting.logResult("info", "<b>Check hotspot with DataConn on.</b>")
        self.settings.enable_hotSpot()

        time.sleep(3)
        self.settings.disable_hotSpot()
