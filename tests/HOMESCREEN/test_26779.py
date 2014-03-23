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

    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)

        self.UTILS = UTILS(self)
        self.EME = EverythingMe(self)
        self.Settings = Settings(self)

        self.UTILS.app.setPermission('Homescreen', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Due to a bug, the message only appears if you
        # have used eme with a network connection first,
        # but not if the first time you use eme is without
        # a network connection. So test for both situations.
        #

        #
        # Launch the 'everything.me' app.
        #
        self.UTILS.reporting.logResult("info", "Launching EME with NO network connection first ...")
        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        #
        # Select a category (group).
        #
        self.EME.pick_group("Games")

        #
        # Verify that the message is displayed.
        #
        self.UTILS.element.waitForElements(DOM.EME.connection_warning_msg,
                                   "Connection message (without using with a network first)",
                                   True, 10, False)

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point:", x)

        #
        # Return home, turn on networking navigate to the group again, then return home.
        #
        self.UTILS.reporting.logResult("info", "Using EME with networking ...")
        self.UTILS.home.scrollHomescreenRight()
        self.UTILS.network.getNetworkConnection()
        self.EME.launch()
        self.EME.pick_group("Social")
        self.UTILS.home.scrollHomescreenRight()

        #
        # Turn networking off and launch the 'everything.me' app again.
        #
        self.UTILS.network.disableAllNetworkSettings()
        self.UTILS.reporting.logResult("info", "Launching EME with NO network connection "\
                                       "(after being used WITH a network connection) ...")
        self.EME.launch()

        #
        # Select a category (group).
        #
        self.EME.pick_group("Music")

        #
        # Verify that the message is displayed.
        #
        self.UTILS.element.waitForElements(DOM.EME.connection_warning_msg,
                                   "Connection message (after using with a network)",
                                   True, 10, False)

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point:", x)
