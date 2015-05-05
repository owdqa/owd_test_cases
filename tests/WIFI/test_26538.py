#===============================================================================
# 26538: Try to turn Wi-Fi HotSpot on when the device has Data connection off
#===============================================================================

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
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
        self.data_layer.connect_to_cell_data()
        self.settings.launch()
        self.settings.hotspot()
        hotspot_settings_btn = self.UTILS.element.getElement(DOM.Settings.hotspot_settings, "Hotspot settings button",
                                                             timeout=20)
        self.UTILS.test.test(hotspot_settings_btn.get_attribute("disabled"), "Hotspot button is disabled.")
        time.sleep(5)
