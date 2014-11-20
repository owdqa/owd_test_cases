
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

        self.wifi_name = self.UTILS.general.get_config_variable("GLOBAL_WIFI_NAME")
        self.wifi_user = self.UTILS.general.get_config_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass = self.UTILS.general.get_config_variable("GLOBAL_WIFI_PASSWORD")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.disable_wifi()
        self.UTILS.element.waitForNotElements(DOM.Statusbar.wifi, "Wifi icon in statusbar")
        self.UTILS.test.test(not self.UTILS.network.is_network_type_enabled("wifi"),
                         "Wifi is disabled before we start this test.")

        self.UTILS.statusbar.toggleViaStatusBar("wifi")
        # If required, connect to the wifi.
        self.marionette.switch_to_frame()
        try:
            self.wait_for_element_present("xpath", "//iframe[contains(@{},'{}')]".\
                                          format(DOM.Settings.frame_locator[0], DOM.Settings.frame_locator[1]),
                                          timeout=10)

            #
            # We need to supply the login details for the network.
            #
            self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)
            self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
            self.marionette.switch_to_frame()
        except:
            pass

        self.UTILS.element.waitForElements(DOM.Statusbar.wifi, "Wifi icon in statusbar", True, 20, False)
        self.UTILS.statusbar.toggleViaStatusBar("wifi")
        self.UTILS.element.waitForNotElements(DOM.Statusbar.wifi, "Wifi icon in statusbar")
