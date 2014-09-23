#===============================================================================
# 26560: Connected Network Details Dialog
#
# Pre-requisites:
# There should be any available network open or secure
#
# Procedure:
# 1- On device under test activate Wi-Fi
# 2- Connect to an available network found
# 3- Once the connection process ends successfully and the network
# appears as connected, tap on its name
# 4- Verify that the Network details page is open showing correct
# information about the network
# 5- Verify also, that there is an option to "Forget this network"
#
# Expected results:
# It is possible to check the details of the network that the device is
# connected to by tapping on its name once the connection has been done
# correctly.
# In this page there is also available an option to "Forget this network"
#===============================================================================
import time
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
        #
        # Open the Settings application.
        #
        self.settings.launch()
        self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
        network = {'ssid': self.wifi_name}
        self.wait_for_condition(lambda m: self.data_layer.is_wifi_connected(network), timeout=30)

        #
        # Return to this wifi and check the details, giving some seconds for the
        # device to get an IP address
        #
        time.sleep(10)
        self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)
        self.settings.wifi_list_tapName(self.wifi_name)

        self.UTILS.element.waitForElements(DOM.Settings.wifi_details_header, "Wifi Details header")
        _forget = self.UTILS.element.getElement(DOM.Settings.wifi_details_forget_btn,
                                                "Details for connected wifi - forget button")
        _ip = self.UTILS.element.getElement(DOM.Settings.wifi_details_ipaddress,
                                            "Details for connected wifi - ip address")
        _link = self.UTILS.element.getElement(DOM.Settings.wifi_details_linkspeed,
                                              "Details for connected wifi - link speed")
        _sec = self.UTILS.element.getElement(DOM.Settings.wifi_details_security,
                                             "Details for connected wifi - security")
        _signal = self.UTILS.element.getElement(DOM.Settings.wifi_details_signal,
                                                "Details for connected wifi - signal")

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot: ", screenshot)
