#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    _GROUP_NAME  = "Games"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)

        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        self.EME        = EverythingMe(self)

        #
        # Don't prompt me for geolocation (this was broken recently in Gaia, so 'try' it).
        #
        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("(Just FYI) Unable to automatically set Homescreen geolocation permission.")


    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.network.getNetworkConnection()
 
        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        x = self.UTILS.element.getElements(DOM.Home.docked_apps, "Docked app icons", False)
        _boolOK = False
        for i in x:
            if "Browser" in i.get_attribute("aria-label"):
                _boolOK = True
                break

        self.UTILS.test.TEST(_boolOK, "Browser is in the dedicated dock icons.")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot:", x)