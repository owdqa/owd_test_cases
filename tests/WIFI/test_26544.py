# OWD-26544:  [INTER][Wi-Fi] Enable/disable Wi-Fi from settings
# ** Procedure
#       1- Go to settings -> Wi-Fi and enable it
#       2- Check the availabe networks listed below "Available networks"
#       3- Scroll up/dwon the found networks
# ** Expected Results
#       It is possible to enable/disable Wi-Fi from settings menu.
#       Once the Wi-Fi is enable, there should appear the available networks listed
#       below ordered according to the strength of the signal.
#       The device shows an icon next to the found networks indicating if
#       they are free or a password will be required.
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.settings.launch()
        self.settings.wifi()
        self.settings.wifi_switch_on()

        available_networks = self.UTILS.element.getElements(
            DOM.Settings.wifi_available_networks, "Available networks", False)
        self.UTILS.reporting.logResult("info", "Found {} networks".format(len(available_networks)))

        for network in available_networks:
            network_name = network.find_element(*("css selector", "span")).text
            try:
                network.find_element(*("css selector", "aside.secured"))
                network.find_element(*("css selector", "small[data-l10n-id='securedBy']"))
                self.UTILS.reporting.logResult('info', "Network [{}] is secured".format(network_name))
            except:
                self.UTILS.reporting.logResult('info', "Network [{}] is NOT secured".format(network_name))
