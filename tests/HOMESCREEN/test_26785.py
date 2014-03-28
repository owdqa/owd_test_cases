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

#     _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)

        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        self.EME        = EverythingMe(self)

        self.UTILS.app.setPermission('Homescreen', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        _appName = "Juegos Gratis"

        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.network.getNetworkConnection()
        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)
        self.UTILS.app.uninstallApp(_appName)

        #
        # Launch the 'everything.me' app.
        #
        self.UTILS.reporting.logResult("info", "Launching EME ...")
        self.EME.launch()
        self.EME.bookmark_app(_appName)

