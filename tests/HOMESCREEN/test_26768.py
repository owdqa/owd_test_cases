#===============================================================================
# 26768: Verify that there is an icon to launch the browser application
#
# Procedure:
# 1- Verify there is a dedicated icon for the browser
#
# Expected result:
# The icon is found
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)

        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.EME = EverythingMe(self)

        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.error("Unable to automatically set Homescreen geolocation permission.")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Make sure 'things' are as we expect them to be first.
        self.connect_to_network()

        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        browser = self.marionette.find_element('css selector', DOM.Home.app_icon_css_selector.format('search'))
        self.UTILS.test.test(browser, "An icon for the browser application was found")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot:", x)
