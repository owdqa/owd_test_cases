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


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.Settings = Settings(self)
        self.Browser = Browser(self)

        self.wifi_name = self.UTILS.general.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user = self.UTILS.general.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass = self.UTILS.general.get_os_variable("GLOBAL_WIFI_PASSWORD")

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Open the Settings application.
        #
        self.Settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
        self.marionette.execute_script("document.getElementById('{}').scrollIntoView();".\
                                       format(DOM.Settings.wifi_advanced_btn[1]))
        x = self.UTILS.element.getElement(DOM.Settings.wifi_advanced_btn, "Advanced settings")
        x.tap()

        self.UTILS.element.waitForElements(DOM.Settings.wifi_advanced_mac, "Mac address")
        self.UTILS.element.waitForElements(DOM.Settings.wifi_advanced_knownNets, "Known networks")
        self.UTILS.element.waitForElements(DOM.Settings.wifi_advanced_joinHidden, "Join hidden network button")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point:", x)

        x = self.UTILS.element.getElements(DOM.Settings.wifi_advanced_knownNets,
                                           "Known networks (should only be 1).")[0]
        x.tap()

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point:", x)

        self.UTILS.element.waitForElements(DOM.Settings.wifi_advanced_forgetBtn, "'Forget network' button")
        self.UTILS.element.waitForElements(DOM.Settings.wifi_advanced_cancelBtn, "'Cancel' button")
