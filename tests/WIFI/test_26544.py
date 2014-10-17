#===============================================================================
# 26544: Enable/disable Wi-Fi from settings
#
# Pre-requisites:
# There should be Wi-Fi networks available
#
# Procedure:
# 1- Go to settings -> Wi-Fi and enable it
# 2- Check the available networks listed below "Available networks"
# 3- Scroll up/down the found networks
#
# Expected results:
# It is possible to enable/disable Wi-Fi from settings menu.
# Once the Wi-Fi is enabled, the available networks should be listed below
# ordered according to the strength of the signal. The device shows an icon next to
# the found networks indicating if they are open or a password will be required.
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Open the Settings application.
        #
        self.settings.launch()
        self.settings.wifi()
        self.settings.wifi_switchOn()

        available_networks = self.UTILS.element.getElements(DOM.Settings.wifi_available_networks, "Available networks")

        self.UTILS.reporting.logResult("info", "Found {} networks".format(len(available_networks)))
        self.UTILS.debug.savePageHTML('/tmp/tests/test_123/wifi.html')

        for net in available_networks:
            _secure1 = False
            _secure2 = False

            self.UTILS.reporting.debug("*** Searching for 'secured' element")
            try:
                self.marionette.find_element("css selector", ".secured", net.id)
                _secure1 = True
            except:
                pass
            self.UTILS.reporting.debug("Secured element: {}".format(_secure1))
            self.UTILS.reporting.debug("*** Searching for 'securedBy' element")
            try:
                self.marionette.find_element("css selector", "small[data-l10n-id=securedBy]", net.id)
                _secure2 = True
            except:
                pass

            self.UTILS.reporting.debug("SecuredBy element: {}".format(_secure2))
            self.UTILS.reporting.debug("*** Searching for network name")
            try:
                _name = self.marionette.find_element("css selector", "a", net.id).text
            except:
                _name = None
            self.UTILS.reporting.debug("Network name: {}".format(_name))

            if _name:
                self.UTILS.test.TEST(_secure1 == _secure2,
                                     "Network '{}' has matching 'network is secured' details ({} "\
                                     "for icon and {} for description).".format(_name, _secure1, _secure2))
