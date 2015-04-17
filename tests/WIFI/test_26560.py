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
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.browser import Browser


class test_main(PixiTestCase):

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.Browser = Browser(self)

        self.wifi_name = self.UTILS.general.get_config_variable("ssid", "wifi")
        self.wifi_pass = self.UTILS.general.get_config_variable("password", "wifi")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Open the Settings application.
        #
        self.settings.launch()
        self.settings.wifi()
        self.settings.connect_to_wifi(self.wifi_name, self.wifi_pass)
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
