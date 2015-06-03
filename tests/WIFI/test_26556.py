#===============================================================================
# 26556: Lock/unlock the device during a Wi-Fi session
#
# Pre-requisites:
# There should be an available Wi-Fi network
#
# Procedure:
# 1- Make a WiFi connection
# 2- Launch a WEB browsing session over Wi-Fi
# 3- Lock the device by pressing the dedicated key
# 4- After a while unlock the device
# 5- Check that the Wi-Fi connection remains active. Confirm browsing to
# another WEB page
#
# Expected results:
# The device is correctly locked/unlocked and the Wi-Fi connection remains
# active.
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
        self.browser = Browser(self)
        self.url1 = "www.google.com"
        self.url2 = "www.wikipedia.org"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()

        # Open the browser app.
        self.browser.launch()
        self.browser.open_url(self.url1)
        self.marionette.switch_to_frame()
        self.browser.wait_for_page_to_load()
        self.UTILS.test.test(self.url1 in self.browser.loaded_url(), "{} successfully loaded".format(self.url1))

        self.device.turn_screen_off()

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Srceenshot of locked screen:", screenshot)

        time.sleep(3)
        self.device.unlock()

        self.browser.open_url(self.url2)
        self.marionette.switch_to_frame()
        self.browser.wait_for_page_to_load()
        self.UTILS.test.test(self.url2 in self.browser.loaded_url(), "{} successfully loaded".format(self.url2))
