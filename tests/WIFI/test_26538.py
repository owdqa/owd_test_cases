#===============================================================================
# 26538: Try to turn Wi-Fi HotSpot on when the device has Data connection off
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(PixiTestCase):

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.settings.launch()
        self.settings.hotSpot()
        hotspot_switch_input = self.UTILS.element.getElement(DOM.Settings.hotspot_switch_input,
                                                             "Hotspot switch input", timeout=20, is_displayed=False)
        self.UTILS.test.test(not hotspot_switch_input.get_attribute("checked"), "Hotspot switch is disabled.")
