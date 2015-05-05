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
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(SpreadtrumTestCase):

    def setUp(self):
        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()
        self.settings.launch()

        # Tap hotspot.
        self.settings.hotspot()

        self.UTILS.reporting.logResult("info", "<b>Check hotspot with WIFI on.</b>")
        self.settings.enable_hotspot()

        time.sleep(3)
        self.settings.disable_hotspot()
        self.UTILS.network.disableAllNetworkSettings()

        self.apps.kill_all()
        time.sleep(2)

        self.data_layer.connect_to_cell_data()
        self.settings.launch()
        self.UTILS.reporting.logResult("info", "<b>Check hotspot with DataConn on.</b>")
        time.sleep(2)
        self.settings.hotspot()
        self.settings.enable_hotspot()

        time.sleep(3)
        self.settings.disable_hotspot()
