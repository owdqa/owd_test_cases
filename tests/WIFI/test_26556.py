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
        self.browser = Browser(self)
        self.url1 = "www.google.com"
        self.url2 = "www.wikipedia.org"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()

        #
        # Open the browser app.
        #
        self.browser.launch()
        self.browser.open_url(self.url1)
        self.UTILS.test.test(self.browser.check_page_loaded(self.url1), "{} successfully loaded".format(self.url1))

        self.device.lock()

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Srceenshot of locked screen:", screenshot)

        time.sleep(3)
        self.device.unlock()

        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)
        self.browser.open_url(self.url2)
        self.UTILS.test.test(self.browser.check_page_loaded(self.url2), "{} successfully loaded".format(self.url2))
