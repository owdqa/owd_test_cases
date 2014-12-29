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
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Open the Settings application.
        self.settings.launch()

        # Tap hotspot.
        self.settings.hotSpot()

        hotspot_settings = self.UTILS.element.getElement(DOM.Settings.hotspot_settings, "Hotspot settings")
        self.UTILS.test.test(hotspot_settings.is_enabled(),
                        "Hotspot settings are enabled by default (<b>meaning that 'hotspot' is off</b>).")
