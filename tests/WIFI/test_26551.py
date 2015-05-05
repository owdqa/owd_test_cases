#===============================================================================
# 26551: WEB connection during a Wi-Fi session
#
# Procedure:
# 1- Make a Wi-Fi connection
# 2- The Wi-Fi connection must be done correctly.
# 3- Launch a WEB browsing session over Wi-Fi by the Menu-> Browser.
# 4- Browse several web sites checking that the navigation is working well
#
# Expected result:
# The device must correctly carry out the WEB browsing through the Wi-Fi
# connection.
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.browser import Browser


class test_main(SpreadtrumTestCase):

    def setUp(self):
        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.browser = Browser(self)
        self.url1 = "www.google.com"
        self.url2 = "www.wikipedia.org"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Open the Settings application.
        self.connect_to_network()

        # Open the browser app.
        self.browser.launch()

        # Open our URL.
        self.browser.open_url(self.url1)
        self.marionette.switch_to_frame()
        self.browser.wait_for_page_to_load()
        self.UTILS.test.test(self.url1 in self.browser.loaded_url(), "Web page loaded correctly.")

        self.browser.open_url(self.url2)
        self.marionette.switch_to_frame()
        self.browser.wait_for_page_to_load()
        self.UTILS.test.test(self.url2 in self.browser.loaded_url(), "Web page loaded correctly.")
