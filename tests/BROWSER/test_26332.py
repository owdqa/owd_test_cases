from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.browser = Browser(self)

        self.wifi_name = self.UTILS.general.get_config_variable("GLOBAL_WIFI_NAME")
        self.wifi_user = self.UTILS.general.get_config_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass = self.UTILS.general.get_config_variable("GLOBAL_WIFI_PASSWORD")

        self.testURL = self.UTILS.general.get_config_variable("GLOBAL_TEST_URL")

        # switch off keyboard FTU screen
        self.data_layer.set_setting("keyboard.ftu.enabled", False)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Forget all networks (so we have to chose one).
        # Roy- *might* want this, but if we're already connected then this is a 'pass' anyway.
        # self.data_layer.forget_all_networks()

        #
        # Open the settings application.
        #
        self.settings.launch()

        #
        # Connect to the wifi.
        #
        self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)

        #
        # Open the browser app.
        #
        self.browser.launch()

        #
        # Open our URL.
        #
        self.browser.open_url(self.testURL)
