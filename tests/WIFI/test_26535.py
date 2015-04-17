#===============================================================================
# 26535: Verify that Wi-Fi HotSpot is disable by default
#
# Procedure:
# 1. Turn the device on
# 2. Go to Settings, under Network & Connectivity check this setting: HotSpot
#
# Expected results:
# Wi-Fi HotSpot is disabled by default when switching on the device
#===============================================================================
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(PixiTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Open the Settings application.
        #
        self.settings.launch()

        #
        # Tap hotspot.
        #
        self.settings.hotSpot()

        x = self.UTILS.element.getElement(DOM.Settings.hotspot_settings, "Hotspot settings")
        self.UTILS.test.test(x.get_attribute("disabled") != "disabled",
                        "Hotspot settings are enabled by default (<b>meaning that 'hotspot' is off</b>).")
