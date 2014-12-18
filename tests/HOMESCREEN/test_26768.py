#===============================================================================
# 26768: Verify that there is an icon to launch the browser application
#
# Procedure:
# 1- Verify there is a dedicated icon for the browser
#
# Expected result:
# The icon is found
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)

        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.EME = EverythingMe(self)

        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.error("Unable to automatically set Homescreen geolocation permission.")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Make sure 'things' are as we expect them to be first.
        self.connect_to_network()

        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        browser = self.marionette.find_element('xpath', DOM.Home.app_icon_xpath.format('browser'))
        self.UTILS.test.test(browser, "An icon for the browser application was found")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot:", x)
