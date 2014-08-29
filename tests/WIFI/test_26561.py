#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.browser import Browser
import time


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
        self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)

        #
        # Return to this wifi and forget it.
        #
        self.settings.wifi_list_tapName(self.wifi_name)
        self.settings.wifi_forget()

        self.UTILS.test.TEST(self.settings.wifi_list_isNotConnected(self.wifi_name),
                             "{} is no longer connected".format(self.wifi_name))

        #
        # make sure we need to add the details again.
        #
        self.settings.wifi_list_tapName(self.wifi_name)
        time.sleep(1)
        self.UTILS.element.waitForElements(DOM.Settings.wifi_login_pass, "Password field")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot after forgetting network: ", x)
