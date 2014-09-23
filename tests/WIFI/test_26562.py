#===============================================================================
# 26562: Advanced Settings menu is available
#
# Procedure:
# 1- On device under test turn Wi-Fi on
# 2- Connect to an available network
# 3- Once the connection process finishes correctly, tap on Advanced Settings
# 4- Verify that it is possible to see info presented there and that it is
# correct
#
# Expected results:
# User should be able to open Advanced Setup menu. There he should be able to find:
# -The MAC information
# -The known networks under the label Saved networks. Tapping on any of them, the
# details dialog menu is open
# -An option to Join Hidden Network
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.browser import Browser


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.Browser = Browser(self)

        self.wifi_name = self.UTILS.general.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user = self.UTILS.general.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass = self.UTILS.general.get_os_variable("GLOBAL_WIFI_PASSWORD")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.settings.launch()
        self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
        network = {'ssid': self.wifi_name}
        self.wait_for_condition(lambda m: self.data_layer.is_wifi_connected(network), timeout=30)

        self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)
        manage_networks = self.marionette.find_element(*DOM.Settings.wifi_advanced_btn)
        self.UTILS.element.scroll_into_view(manage_networks)
        self.UTILS.element.waitForElements(DOM.Settings.wifi_advanced_btn, "Waiting for advanced wifi settings",
                                           timeout=30)
        btn = self.UTILS.element.getElement(DOM.Settings.wifi_advanced_btn, "Advanced settings")
        btn.tap()

        self.UTILS.element.waitForElements(DOM.Settings.wifi_advanced_mac, "Mac address")
        self.UTILS.element.waitForElements(DOM.Settings.wifi_advanced_knownNets, "Known networks")
        self.UTILS.element.waitForElements(DOM.Settings.wifi_advanced_joinHidden, "Join hidden network button")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point:", x)

        x = self.UTILS.element.getElements(DOM.Settings.wifi_advanced_knownNets,
                                           "Known networks (should only be 1).")[0]
        x.tap()

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point:", x)

        self.UTILS.element.waitForElements(DOM.Settings.wifi_advanced_forgetBtn, "'Forget network' button")
        self.UTILS.element.waitForElements(DOM.Settings.wifi_advanced_cancelBtn, "'Cancel' button")
        forget_btn = self.marionette.find_element(*DOM.Settings.wifi_advanced_forgetBtn)
        forget_btn.tap()
