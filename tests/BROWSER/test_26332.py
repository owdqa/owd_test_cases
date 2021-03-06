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

        self.wifi_name = self.UTILS.general.get_config_variable("ssid", "wifi")
        self.wifi_pass = self.UTILS.general.get_config_variable("password", "wifi")

        self.testURL = self.UTILS.general.get_config_variable("test_url", "common")
        self.apps.set_permission_by_url(Browser.search_manifest_url, 'geolocation', 'deny')

        # switch off keyboard FTU screen
        self.data_layer.set_setting("keyboard.ftu.enabled", False)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Open the settings application.
        self.settings.launch()

        # Connect to the wifi.
        self.settings.wifi()
        self.settings.connect_to_wifi(self.wifi_name, self.wifi_pass)

        # Open the browser app.
        self.browser.launch()
        # Open our URL.
        self.browser.open_url(self.testURL)
